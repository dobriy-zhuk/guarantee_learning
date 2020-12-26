from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, CreateLessonForm
from django.contrib.auth.decorators import login_required
from .models import Teacher, Student, Module, Lesson
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
import json
from django.http import JsonResponse
from json import dumps

@login_required
def box(request):
    lessons = []
    all_lessons = Lesson.objects.distinct()
    for lesson in all_lessons:
        cur = lesson.students.filter(user=request.user)
        if cur.exists():
            lessons.append(lesson)

    student = Student.objects.filter(user=request.user)

    return render(request, 'box.html', {'lessons': lessons, 'student': student })


def new_lesson(request):
    #posts = Post.objects.all()
    response_data = {}
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    modules = Module.objects.all()

    if request.POST.get('action') == 'post':
        title = request.POST.get('title')
        description = request.POST.get('students')

        response_data['title'] = "title"
        response_data['description'] = description

        #Post.objects.create(
        #    title=title,
        #    description=description,
        #)
        return JsonResponse(response_data)

    return render(request, 'new_lesson.html', {
        'students': students,
        'teachers': teachers,
        'modules': modules
    })


@login_required
def lesson(request):
    return render(request, 'lesson.html', {})


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
def finish_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    response_data = {}
    if request.POST.get('action') == 'post':
        homework = request.POST.get('homework')
        infoJson = request.body
        print(infoJson)
        lesson.finished = True
        lesson.homework = homework
        lesson.save()
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
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

