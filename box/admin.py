from django.contrib import admin
from .models import Student, Teacher, Module, Lesson
from .forms import CreateLessonForm
from django.contrib.admin import site, ModelAdmin

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Module)
admin.site.register(Lesson)
