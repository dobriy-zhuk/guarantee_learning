"""guarantee_learning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('school/', views.school, name='school'),
    path('contact/', views.contact, name='contact'),
    path('demo/', views.demo_lesson, name='demo'),
    path('camp/', views.camp, name='camp'),
    path('coding/', views.coding, name='coding'),
    path('robotics/', views.robotics, name='robotics'),
    path('school_subjects/', views.school_subjects, name='school_subjects'),
    path('exams/', views.exams, name='exams'),
]
