from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=100)
    currency = models.CharField(max_length=4)
    #status = models.CharField(max_length=100)
    #phone = models.CharField(max_length=100)
    bonus = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'students'

    def __str__(self):
        return self.user.first_name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=100)
    currency = models.CharField(max_length=4)
    #phone = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'teachers'

    def __str__(self):
        return self.user.first_name


class Module(models.Model):
    title = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'modules'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    start = models.DateTimeField(default=now,blank=True)
    end = models.DateTimeField(default=now,blank=True)
    homework = models.TextField()
#    info_about_kids = models.TextField()
    link = models.CharField(max_length=400, default="your link here")
    finished = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'lessons'

    def __str__(self):
        return self.name

