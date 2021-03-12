from django.contrib import admin
from .models import Student, Teacher, Module, Lesson, LessonInfo, Subject, Manager, Branch, StudentStatus, Task, KPI, Finance
from django.contrib.admin import site, ModelAdmin

admin.site.register(Manager)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Module)
admin.site.register(Branch)
admin.site.register(StudentStatus)
admin.site.register(Lesson)
admin.site.register(LessonInfo)
admin.site.register(Task)
admin.site.register(KPI)
admin.site.register(Finance)
