from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import JsonResponse
from django.core.mail import send_mail
from .models import MetaText


def index(request):
    return render(request, 'index.html', {})


def school(request):
    return render(request, 'school.html', {})


def camp(request):
    return render(request, 'main_site/camp.html', {})


def coding(request):
    meta_obj = get_object_or_404(MetaText, name="coding")
    return render(request, 'main_site/coding.html', {"this_page": meta_obj})


def school_subjects(request):
    meta_obj = get_object_or_404(MetaText, name="school_subjects")
    return render(request, 'main_site/school_subjects.html', {"this_page": meta_obj})


def exams(request):
    meta_obj = get_object_or_404(MetaText, name="exams")
    return render(request, 'main_site/exams.html', {"this_page": meta_obj})


def robotics(request):
    meta_obj = get_object_or_404(MetaText, name="robotics")
    return render(request, 'main_site/robotics.html', {"this_page": meta_obj})


def contact(request):
    response_data = {}
    meta_obj = get_object_or_404(MetaText, name="contacts")

    if request.POST.get('action') == 'post':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        place = request.POST.get('place')
        comment = request.POST.get('comment')


        # Post.objects.create( ДОБАВИТЬ В БАЗУ!!!
        #    title=title,
        #    description=description,
        # )
        body = "Новая заявка от клиента\nИмя: " + name + "\nEmail: " + email + "\nТелефон: " + phone + "\nПредмет: " + subject + "\nМесто проведения: " + place + " \nКомментарий: " + comment

        if name and phone and email:
            try:
                send_mail("Заявка с вашего сайта от клиента", body, email, ['info@garantylearning.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            response_data['result'] = "Ваша заявка отправлена. Мы свяжемся с вами в ближайшее время!"
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            response_data['result'] = "Проверьте корректность введенных данных!"

        return JsonResponse(response_data)

    return render(request, 'main_site/contact.html', {"this_page": meta_obj})


def demo_lesson(request):
    response_data = {}
    meta_obj = get_object_or_404(MetaText, name="demo_lesson")

    if request.POST.get('action') == 'post':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        demo_date = request.POST.get('demo_date')
        comment = request.POST.get('comment')


        # Post.objects.create( ДОБАВИТЬ В БАЗУ!!!
        #    title=title,
        #    description=description,
        # )
        body = "Запись на вводный урок\nИмя: " + name + "\nEmail: " + email + "\nТелефон: " + phone + "\nПредмет: " + subject + "\nВремя проведения: " + demo_date + " \nКомментарий: " + comment

        if name and phone and email:
            try:
                send_mail("Запись на вводный урок от клиента", body, email, ['info@garantylearning.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            response_data['result'] = "Ваша заявка отправлена. Мы свяжемся с вами в ближайшее время!"
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            response_data['result'] = "Проверьте корректность введенных данных!"

        return JsonResponse(response_data)

    return render(request, 'main_site/demo_lesson.html', {"this_page": meta_obj})
