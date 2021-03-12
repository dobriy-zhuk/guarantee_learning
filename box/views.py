from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from .forms import LoginForm, CreateLessonForm
from django.contrib.auth.decorators import login_required
from .models import Teacher, Student, Module, Lesson, Subject, Manager, Branch, StudentStatus, KPI, Task, Finance
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
import json
from django.http import JsonResponse
from json import dumps
from django.utils.dateparse import parse_datetime, parse_date, parse_time
import uuid
from datetime import timedelta, datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings as conf_settings
import requests
import urllib
from .forms import RegisterForm, StudentForm, UserForm, TeacherForm, ManagerForm, ModuleForm, TaskForm, FinanceForm, KPIForm, LessonForm
from django.views.decorators.csrf import csrf_exempt


def box(request):

    if request.user.is_active:
        student = Student.objects.filter(user=request.user).first()
        if student is not None:
            return redirect('student_box')

        teacher = Teacher.objects.filter(user=request.user).first()
        if teacher is not None:
            return redirect('teacher_box')

        manager = Manager.objects.filter(user=request.user).first()
        if manager is not None:
            return redirect('manager_box')
    else:
        return redirect('login')


@login_required
def teacher_box(request):

    teacher = Teacher.objects.get(user=request.user)
    if teacher is not None:
        finished = request.GET.get('finished', False)
        all_lessons = Lesson.objects.filter(teacher=teacher).order_by('start').filter(finished=finished)

        page = request.GET.get('page', 1)
        paginator = Paginator(all_lessons, 10)
        try:
            all_lessons = paginator.page(page)
        except PageNotAnInteger:
            all_lessons = paginator.page(1)
        except EmptyPage:
            all_lessons = paginator.page(paginator.num_pages)

        last_homework = Lesson.objects.filter(finished=True).last()

        return render(request, 'teacher_box/box.html',
                      {'lessons': all_lessons, 'teacher': teacher, 'last_homework': last_homework.homework})
    else:
        return HttpResponse("Не определена роль пользователя")


@login_required
def student_box(request):
    lessons = []
    finished = request.GET.get('finished', False)
    all_lessons = Lesson.objects.all().order_by('start').filter(finished=finished)

    student = Student.objects.filter(user=request.user).first()
    if student is not None:
        for lesson in all_lessons:
            cur = lesson.students.filter(user=request.user)
            if cur.exists():
                lessons.append(lesson)

        page = request.GET.get('page', 1)
        paginator = Paginator(lessons, 10)
        try:
            lessons = paginator.page(page)
        except PageNotAnInteger:
            lessons = paginator.page(1)
        except EmptyPage:
            lessons = paginator.page(paginator.num_pages)

        #last_homework = Lesson.objects.filter(finished=True).last()

        return render(request, 'student_box/box.html',
                      {'lessons': lessons, 'student': student})
    else:
        return HttpResponse("Не определена роль пользователя")


@login_required
def manager_box(request):
    return render(request, 'manager_box/box.html')


def new_lesson(request):

    if request.method == "POST":
        lesson_form = LessonForm(request.POST)
        #lesson_start = parse_datetime(request.POST["lesson_start"])
        #lesson_end = parse_date(request.POST.get("lesson_end", lesson_start))
        lesson_frequency = request.POST["lesson_frequency"]
        lesson_module = Module.objects.all()

        module_number = 1

        if lesson_form.is_valid():

            lesson_start = parse_datetime(lesson_form["start"].value())
            lesson_end = parse_date(request.POST.get("lesson_end", lesson_start))

            while lesson_start.date() <= lesson_end:

                lesson = lesson_form.save(commit=False)
                lesson.start = lesson_start
                lesson.end = lesson_start + timedelta(minutes=int(lesson_form["duration"].value()))
                lesson.pk = None
                lesson.save()
                lesson_form.save_m2m()

                if lesson_frequency == "every_week":
                    lesson_start = lesson_start + timedelta(days=7)
                elif lesson_frequency == "every_day":
                    lesson_start = lesson_start + timedelta(days=1)

        return redirect("list_lesson")
    else:
        lesson_form = LessonForm()

    return render(request, "manager_box/new_lesson.html", {"lesson_form": lesson_form, })


'''   
#TODO: change to standard django form!
    response_data = {}
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    subjects = Subject.objects.all()

    if request.method =='POST':
        data = json.loads(request.body.decode('utf-8'))

        lesson_title = data['title']
        lesson_subject = Subject.objects.get(title=data['subject'])
        lesson_module = Module.objects.all()
        lesson_students = data['students']
        lesson_teacher = Teacher.objects.get(pk=data['teachers'][0])
        lesson_start = parse_datetime(data['start'])
        lesson_end = parse_datetime(data['end'])
        lesson_duration = data['duration']
        lesson_frequency = data['frequency']
        #lesson_branch = data['branch']
        lesson_branch = Branch.objects.filter(title="Онлайн").first()

        module_number = 1

        while lesson_start < lesson_end:

            if lesson_frequency == "every_week":
                this_lesson_end = lesson_start + timedelta(minutes=int(lesson_duration))
                lesson = Lesson.objects.create(name=lesson_title, branch=lesson_branch, subject=lesson_subject, module=lesson_module[0], start=lesson_start, end=this_lesson_end,
                                               teacher=lesson_teacher, link=uuid.uuid1())
                for student in lesson_students:
                    my_student = Student.objects.get(pk=student)
                    lesson.students.add(my_student)
                module = Module.objects.filter(module_number=module_number).first()
                if module is not None:
                    lesson.module = module
                lesson.save()
                lesson_start = lesson_start + timedelta(days=7)
                module_number += 1
        #Add link for lesson using time

            elif lesson_frequency == "every_day":
                this_lesson_end = lesson_start + timedelta(minutes=int(lesson_duration))
                lesson = Lesson.objects.create(name=lesson_title, branch=lesson_branch, subject=lesson_subject, module=lesson_module[0], start=lesson_start, end=this_lesson_end,
                                               teacher=lesson_teacher, link=uuid.uuid1())
                for student in lesson_students:
                    my_student = Student.objects.get(pk=student)
                    lesson.students.add(my_student)
                module = Module.objects.filter(module_number=module_number).first()
                if module is not None:
                    lesson.module = module
                lesson.save()
                lesson_start = lesson_start + timedelta(days=1)
                module_number += 1

        response_data['result'] = "Уроки добавлены"



        #Post.objects.create(
        #    title=title,
        #    description=description,
        #)
        return JsonResponse(response_data)

    return render(request, 'manager_box/new_lesson.html', {
        'students': students,
        'teachers': teachers,
        'subjects': subjects
    })
'''

@login_required
def edit_lesson(request, pk):
    subject = request.GET.get('subject', 0)
    lesson = get_object_or_404(Lesson, pk=pk)

    if request.method == "POST":
        lesson_form = LessonForm(request.POST, instance=lesson)

        if lesson_form.is_valid():
            lesson_form.save()

        return redirect("list_lesson")
    else:
        lesson_form = LessonForm(instance=lesson)

    return render(request, "manager_box/edit_lesson.html", {"lesson_form": lesson_form, })




def remove_lesson(request, pk):
    try:

        lesson = get_object_or_404(Lesson, pk=pk)
        lesson.delete()

    except User.DoesNotExist:
        #messages.error(request, "User doesnot exist")
        #return render(request, 'front.html')
        return redirect('list_lesson')

    except Exception as e:
        return redirect('list_lesson', {'err':e.message})

    return redirect('list_lesson')



@login_required
def profile_list(request):

    user_type = request.GET.get('user_type', False)

    all_profiles = Student.objects.all().order_by('user')
    if user_type == "student":
        all_profiles = Student.objects.all().order_by('user')
    elif user_type == "teacher":
        all_profiles = Teacher.objects.all().order_by('user')
    elif user_type == "manager":
        all_profiles = Manager.objects.all().order_by('user')

    page = request.GET.get('page', 1)
    paginator = Paginator(all_profiles, 10)
    try:
        all_profiles = paginator.page(page)
    except PageNotAnInteger:
        all_profiles = paginator.page(1)
    except EmptyPage:
        all_profiles = paginator.page(paginator.num_pages)

    return render(request, 'manager_box/profile_list.html',
                      {'all_profiles': all_profiles})


@login_required
def kpi(request):

    year = request.GET.get('year', 2021)
    client_kpi = KPI.objects.filter(name="Количество клиентов").first()
    leads_kpi = KPI.objects.filter(name="Новые лиды").first()


    return render(request, 'manager_box/kpi.html',
                      {'client_kpi': zip(client_kpi.plan, client_kpi.result),
                       'leads_kpi': zip(leads_kpi.plan, leads_kpi.result),
                       })


@login_required
def edit_kpi(request, pk):
    subject = request.GET.get('subject', 0)
    kpi = get_object_or_404(KPI, pk=pk)

    if request.method == "POST":
        kpi_form = KPIForm(request.POST, instance=kpi)

        if kpi_form.is_valid():
            kpi_form.save()

        return redirect("kpi")
    else:
        kpi_form = KPIForm(instance=kpi)

    return render(request, "manager_box/edit_kpi.html", {"kpi_form": kpi_form, })



@login_required
def edit_profile(request, pk):

    cur_user = get_object_or_404(User, pk=pk)
    profile = None

    student = Student.objects.filter(user=cur_user).first()
    if student is not None:
        profile = student

    teacher = Teacher.objects.filter(user=cur_user).first()
    if teacher is not None:
        profile = teacher

    manager = Manager.objects.filter(user=cur_user).first()
    if manager is not None:
        profile = manager

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=cur_user)
        profile_form = StudentForm(request.POST, instance=profile)
        if teacher is not None:
            profile_form = TeacherForm(request.POST, instance=profile)
        elif manager is not None:
            profile_form = ManagerForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_list')

    else:
        user_form = UserForm(instance=cur_user)

        profile_form = StudentForm(instance=profile)
        if teacher is not None:
            profile_form = TeacherForm(instance=profile)
        elif manager is not None:
            profile_form = ManagerForm(instance=profile)

    return render(request, 'manager_box/edit_profile.html', {'user_form': user_form,
                                                             'profile_form': profile_form,
                                                            }
                  )


def remove_profile(request, pk):
    try:

        cur_user = get_object_or_404(User, pk=pk)
        profile = None

        student = Student.objects.filter(user=cur_user).first()
        if student is not None:
            profile = student

        teacher = Teacher.objects.filter(user=cur_user).first()
        if teacher is not None:
            profile = teacher

        manager = Manager.objects.filter(user=cur_user).first()
        if manager is not None:
            profile = manager

        if not cur_user.is_superuser:
            profile.delete()
            cur_user.delete()
        else:
            pass
            #you cant remove staff!


    except User.DoesNotExist:
        #messages.error(request, "User doesnot exist")
        #return render(request, 'front.html')
        return redirect('profile_list')

    except Exception as e:
        return redirect('profile_list', {'err':e.message})

    return redirect('profile_list')


@csrf_exempt
def new_profile(request):
    profile_type = request.GET.get('profile_type', "student")

    if request.method == "POST":
        user_form = UserForm(request.POST)

        profile_form = StudentForm(request.POST)
        if profile_type == "teacher":
            profile_form = TeacherForm(request.POST)
        elif profile_type == "manager":
            profile_form = ManagerForm(request.POST)

        if profile_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            if profile_type == "teacher":
                group = Group.objects.get(name='teacher')
                group.user_set.add(user)
            elif profile_type == "manager":
                pass

        return redirect("profile_list")
    else:
        user_form = UserForm()

        profile_form = StudentForm()
        if profile_type == "teacher":
            profile_form = TeacherForm()
        elif profile_type == "manager":
            profile_form = ManagerForm()

    return render(request, "manager_box/new_profile.html", {"user_form": user_form, "profile_form": profile_form,})



@login_required
def list_lesson(request):
    manager = Manager.objects.filter(user=request.user).first()
    if manager is not None:
        finished = request.GET.get('finished', False)
        branch = request.GET.get('branch', 1)
        teacher = request.GET.get('teacher', 0)
        all_lessons = Lesson.objects.all().order_by('start').filter(finished=finished, branch=branch)
        if teacher != str(0):
            all_lessons = Lesson.objects.all().order_by('start').filter(finished=finished, branch=branch, teacher=teacher)

        page = request.GET.get('page', 1)
        paginator = Paginator(all_lessons, 10)
        try:
            all_lessons = paginator.page(page)
        except PageNotAnInteger:
            all_lessons = paginator.page(1)
        except EmptyPage:
            all_lessons = paginator.page(paginator.num_pages)

        return render(request, 'manager_box/list_lesson.html',
                      {'lessons': all_lessons, 'manager': manager, 'branches': Branch.objects.all(), 'teachers': Teacher.objects.all() })
    else:
        return HttpResponse("Не определена роль пользователя")



def payment(request):
    #TODO: check if cant pay and need help to pay

    AMOUNT = 0

    payment_username = conf_settings.PAYMENT_USERNAME
    payment_password = conf_settings.PAYMENT_PASSWORD
    payment_gateway_url = conf_settings.PAYMENT_GATEWAY_URL
    payment_return_url = conf_settings.PAYMENT_RETURN_URL

    def gateway(method, data):
        response = requests.post(payment_gateway_url + method, data=urllib.parse.urlencode(data), headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'})
        result = json.loads(response.content)
        return result

    if request.method == 'POST':
        AMOUNT = request.POST.get("sum")

        data = {
            'userName': payment_username,
            'password': payment_password,
            'orderNumber': datetime.now().timestamp(),
            'description': '{0} {1} ({2})'.format(request.user.first_name, request.user.last_name, request.user),
            'amount': AMOUNT,
            'returnUrl': payment_return_url
             }

        response = gateway("register.do", data)
        return redirect(response['formUrl'])

    if 'orderId' in request.GET:

        data = {
            'userName': payment_username,
            'password': payment_password,
            'orderId': request.GET['orderId']
        }

        response = gateway("getOrderStatusExtended.do", data)
        print(response)
        if response['actionCode'] == 0:
            amount = response['amount'] / 100

            if request.user.is_authenticated:
                print(request.user)
                cur_user = get_object_or_404(User, username=request.user)

                student = Student.objects.filter(user=cur_user).first()

                if student is not None:
                    finance = Finance.objects.create(title="Платеж от клиента", orderId=response['orderNumber'], amount=amount, user_added=cur_user, comment=response['orderDescription'])
                    finance.save()

                    student.amount += amount
                    student.save()

                else:
                    finance = Finance.objects.create(title="Платеж от клиента", orderId=response['orderNumber'],
                                                     amount=amount, user_added=cur_user,
                                                     comment=response['orderDescription'])
                    finance.save()

            else:
                finance = Finance.objects.create(title="Платеж от клиента", orderId=response['orderNumber'], amount=amount,
                                                 user_added=request.user, comment=response['orderDescription'])
                finance.save()

            return redirect('box')

    return render(request, 'payment.html', {})


def test(request):
    if request.user.is_authenticated:

        cur_user = get_object_or_404(User, username=request.user)

        student = Student.objects.filter(user=cur_user).first()
        if student is not None:
            finance = Finance.objects.create(title="Платеж от клиента", orderId="123123",
                                             amount=100, user_added=cur_user,
                                             comment="asdasd")
            finance.save()

            if cur_user.groups.filter(name="student").exists():
                student.amount += 100
                student.save()


    return redirect('box')



@login_required
def change_bonus(request):

    response_data = {}

    if request.POST.get('action') == 'post':
        bonus = request.POST.get('bonus')
        user_email = request.POST.get('email')
        username = User.objects.get(username__iexact=user_email)
        student = get_object_or_404(Student, user__exact = username)
        student.bonus += bonus
        student.save()

        response_data['student'] = student.bonus

        #Post.objects.create(
        #    title=title,
        #    description=description,
        #)
    return JsonResponse(response_data)



@login_required
def current_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    return render(request, 'current_lesson.html', {'lesson': lesson})


@login_required
def whiteboard(request):
    return render(request, 'white_board.html', {})


@login_required
def finish_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    subject = Subject.objects.get(title=lesson.subject)
    current_teacher = Teacher.objects.get(user=lesson.teacher.user)
    response_data = {}
    if request.POST.get('action') == 'post':
        homework = request.POST.get('homework')
        infoJson = json.loads(request.POST.get('students'))
        for student_visited in infoJson:
            current_student = get_object_or_404(Student, user__username=student_visited['key'])
            if int(student_visited['value']) >= 0:
                current_student.bonus += int(student_visited['value'])
                current_student.amount = current_student.amount - subject.price
            elif int(student_visited['value']) == -2:
                current_student.amount = current_student.amount - subject.price
            current_student.save()
        lesson.finished = True
        lesson.homework = homework
        lesson.save()
        current_teacher.salary += current_teacher.hourly_rate
        current_teacher.save()
        response_data['result'] = "ok"

    else:
        response_data['result'] = "error"

    return JsonResponse(response_data)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/box/')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('/')


def registration(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            student = Student.objects.create(user=user)
            student.save()

        return redirect("box")
    else:
        form = RegisterForm()

    return render(response, "registration.html", {"form": form})


### MODULES ###
@login_required
def module_list(request):

    subject = request.GET.get('subject', "Программирование Kodu")

    module_list = Module.objects.filter(subject__title=subject).order_by('module_number')
    subjects = Subject.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(module_list, 10)
    try:
        module_list = paginator.page(page)
    except PageNotAnInteger:
        module_list = paginator.page(1)
    except EmptyPage:
        module_list = paginator.page(paginator.num_pages)

    return render(request, 'manager_box/module_list.html',
                      {'module_list': module_list, 'subjects': subjects})

@login_required
def new_module(request):
    subject = request.GET.get('subject', 0)

    if request.method == "POST":
        module_form = ModuleForm(request.POST)

        if module_form.is_valid():
            module_form.save()

        return redirect("module_list")
    else:
        module_form = ModuleForm()

    return render(request, "manager_box/new_module.html", {"module_form": module_form, })


@login_required
def edit_module(request, pk):
    subject = request.GET.get('subject', 0)
    module = get_object_or_404(Module, pk=pk)

    if request.method == "POST":
        module_form = ModuleForm(request.POST, instance=module)

        if module_form.is_valid():
            module_form.save()

        return redirect("module_list")
    else:
        module_form = ModuleForm(instance=module)

    return render(request, "manager_box/edit_module.html", {"module_form": module_form, })


@login_required
def remove_module(request, pk):
    try:
        module = get_object_or_404(Module, pk=pk)
        module.delete()
    except Module.DoesNotExist:
        #messages.error(request, "User doesnot exist")
        #return render(request, 'front.html')
        return redirect('module_list')

    except Exception as e:
        return redirect('module_list', {'err':e.message})

    return redirect('module_list')



### TASKS ###
@login_required
def task_list(request):

    subject = request.GET.get('subject', "Программирование Kodu")

    task_list = Task.objects.all()

    subjects = Subject.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(task_list, 10)
    try:
        task_list = paginator.page(page)
    except PageNotAnInteger:
        task_list = paginator.page(1)
    except EmptyPage:
        task_list = paginator.page(paginator.num_pages)

    return render(request, 'manager_box/task_list.html',
                      {'task_list': task_list, 'subjects': subjects})

@login_required
def new_task(request):
    subject = request.GET.get('subject', 0)

    if request.method == "POST":
        task_form = TaskForm(request.POST)

        if task_form.is_valid():
            task_form.save()

        return redirect("task_list")
    else:
        task_form = TaskForm()

    return render(request, "manager_box/new_task.html", {"task_form": task_form, })


@login_required
def edit_task(request, pk):
    subject = request.GET.get('subject', 0)
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        task_form = TaskForm(request.POST, instance=task)

        if task_form.is_valid():
            task_form.save()

        return redirect("task_list")
    else:
        task_form = TaskForm(instance=task)

    return render(request, "manager_box/edit_task.html", {"task_form": task_form })


@login_required
def remove_task(request, pk):
    try:
        task = get_object_or_404(Task, pk=pk)
        task.delete()
    except Task.DoesNotExist:
        #messages.error(request, "User doesnot exist")
        #return render(request, 'front.html')
        return redirect('task_list')

    except Exception as e:
        return redirect('task_list', {'err':e.message})

    return redirect('task_list')



### FINANCES ###
@login_required
def finance_list(request):

    finance_list = Finance.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(finance_list, 30)
    try:
        finance_list = paginator.page(page)
    except PageNotAnInteger:
        finance_list = paginator.page(1)
    except EmptyPage:
        finance_list = paginator.page(paginator.num_pages)

    return render(request, 'manager_box/finance_list.html',
                      {'finance_list': finance_list})


@login_required
def new_finance(request):
    subject = request.GET.get('subject', 0)

    if request.method == "POST":
        finance_form = FinanceForm(request.POST)

        if finance_form.is_valid():
            finance_form.save()

        return redirect("finance_list")
    else:
        finance_form = FinanceForm()

    return render(request, "manager_box/new_finance.html", {"finance_form": finance_form, })


@login_required
def edit_finance(request, pk):
    subject = request.GET.get('subject', 0)
    finance = get_object_or_404(Finance, pk=pk)

    if request.method == "POST":
        finance_form = FinanceForm(request.POST, instance=finance)

        if finance_form.is_valid():
            finance_form.save()

        return redirect("finance_list")
    else:
        finance_form = FinanceForm(instance=finance)

    return render(request, "manager_box/edit_finance.html", {"finance_form": finance_form })


@login_required
def remove_finance(request, pk):
    try:
        finance = get_object_or_404(Finance, pk=pk)
        finance.delete()
    except Finance.DoesNotExist:
        #messages.error(request, "User doesnot exist")
        #return render(request, 'front.html')
        return redirect('finance_list')

    except Exception as e:
        return redirect('finance_list', {'err':e.message})

    return redirect('finance_list')