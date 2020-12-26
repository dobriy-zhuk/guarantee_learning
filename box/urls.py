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
    path('', views.box, name='box'),
    path('login/', views.user_login, name='login'),
    path('lesson/', views.lesson, name='lesson'),
    path('lesson/<int:pk>/', views.current_lesson, name='current_lesson'),
    #path('lesson/<int:pk>/edit', views.edit_lesson, name='edit_lesson'),
    path('lesson/<int:pk>/finish/', views.finish_lesson, name='finish_lesson'),
    path('lesson/new/', views.new_lesson, name='new_lesson'),
    path('lesson/change_bonus/', views.change_bonus, name='change_bonus'),
]
