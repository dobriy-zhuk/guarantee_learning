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

    path('accounts/login/', views.user_login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.user_logout, name='logout'),

    path('', views.box, name='box'),
    path('student', views.student_box, name='student_box'),
    path('teacher', views.teacher_box, name='teacher_box'),
    path('manager', views.manager_box, name='manager_box'),

    path('profile/new', views.new_profile, name='new_profile'),
    path('profile/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>/edit', views.edit_profile, name='edit_profile'),
    path('profile/<int:pk>/remove', views.remove_profile, name='remove_profile'),

    path('lessons/', views.list_lesson, name='list_lesson'),
    path('lesson/<int:pk>/', views.current_lesson, name='current_lesson'),
    path('lesson/<int:pk>/edit', views.edit_lesson, name='edit_lesson'),
    path('lesson/<int:pk>/remove/', views.remove_lesson, name='remove_lesson'),
    path('lesson/<int:pk>/finish/', views.finish_lesson, name='finish_lesson'),
    path('lesson/new/', views.new_lesson, name='new_lesson'),
    path('lesson/change_bonus/', views.change_bonus, name='change_bonus'),
    path('lesson/whiteboard/', views.whiteboard, name='whiteboard'),


    path('module_list/', views.module_list, name='module_list'),
    path('module/new/', views.new_module, name='new_module'),
    path('module/<int:pk>/edit', views.edit_module, name='edit_module'),
    path('module/<int:pk>/remove/', views.remove_module, name='remove_module'),

    path('payment/', views.payment, name='payment'),
    path('test/', views.test, name='test'),

    path('kpi/', views.kpi, name='kpi'),
    path('kpi/<int:pk>/edit', views.edit_kpi, name='edit_kpi'),

    path('task_list/', views.task_list, name='task_list'),
    path('task/new/', views.new_task, name='new_task'),
    path('task/<int:pk>/edit', views.edit_task, name='edit_task'),
    path('task/<int:pk>/remove/', views.remove_task, name='remove_task'),

    path('finance_list/', views.finance_list, name='finance_list'),
    path('finance/new/', views.new_finance, name='new_finance'),
    path('finance/<int:pk>/edit', views.edit_finance, name='edit_finance'),
    path('finance/<int:pk>/remove/', views.remove_finance, name='remove_finance'),



]
