from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import JsonResponse
from django.core.mail import send_mail

def index(request):
    return render(request, 'index.html', {})


def contact(request):
    response_data = {}

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

    return render(request, 'contact.html', {})
