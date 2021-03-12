from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.postgres.fields import ArrayField

import random
import string

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=100, default="")
    bank_details = models.TextField(default="")
    #branch
    # status - archive or not

    class Meta:
        verbose_name_plural = 'managers'

    def __str__(self):
        return "{0} {1}".format(self.user.first_name,self.user.last_name)


class StudentStatus(models.Model):
    title = models.CharField(max_length=30, default="Лид")

    class Meta:
        verbose_name_plural = 'student_statuses'

    def __str__(self):
        return self.title

#class Promotion
#trigger promotion using get params from ads



#class OFD


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)
    currency = models.CharField(max_length=4)
    status = models.ForeignKey(StudentStatus, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, default="")
    bonus = models.PositiveIntegerField(default=0)
    #comment = models.CharField(max_length=500)
    #time_added
    #branches
    #subjects
    #responsible_manager
    #status - archive or not
    #source
    #script of dialog with clients
    #причина отказа
    #promotion = ForeignKey

    class Meta:
        verbose_name_plural = 'students'

    def __str__(self):
        return "{0} {1}".format(self.user.first_name, self.user.last_name)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=100)
    salary = models.IntegerField(default=0)
    hourly_rate = models.IntegerField(default=250)
    currency = models.CharField(max_length=4)
    phone = models.CharField(max_length=100, default="")
    #branch
    #responsible_manager
    #subjects m2m
    #time_added
    #status - archive or not
    #date_added = models.DateTimeField(default=now,blank=True)

    class Meta:
        verbose_name_plural = 'teachers'

    def __str__(self):
        return "{0} {1}".format(self.user.first_name, self.user.last_name)


class Branch(models.Model):
    title = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'branches'

    def __str__(self):
        return self.title


class Subject(models.Model):
    title = models.CharField(max_length=30, blank=True, null=True)
    price = models.IntegerField(default=1000)
    # quality_test_for_teacher

    class Meta:
        verbose_name_plural = 'subjects'

    def __str__(self):
        return self.title


class Module(models.Model):
    title = models.CharField(max_length=30, blank=True, null=True)
    module_number = models.IntegerField(default=0)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student_text = models.TextField(blank=True, null=True)
    teacher_text = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'modules'

    def __str__(self):
        return "{0} ({1})".format(self.title, self.subject)


def meeting_link():
    letters = string.ascii_lowercase
    meeting_str = ''.join(random.choice(letters) for i in range(10))
    return meeting_str


class Lesson(models.Model):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, default=0, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ManyToManyField(Teacher)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    start = models.DateTimeField(default=now,blank=True)
    end = models.DateTimeField(default=now,blank=True)
    duration = models.PositiveIntegerField(default=60)
    homework = models.TextField(blank=True)
    link = models.CharField(max_length=400, default=meeting_link, blank=True)
    finished = models.BooleanField(default=False)


    class Meta:
        verbose_name_plural = 'lessons'

    def __str__(self):
        return self.name + " " + str(self.start)


class LessonInfo(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    students_visited = models.ManyToManyField(Student)
    user_changed = models.ForeignKey(User, on_delete=models.CASCADE)
    date_changed = models.DateTimeField(default=now,blank=True)

    def __str__(self):
        return "History: " + str(self.lesson.name)


class Task(models.Model):

    HIGH = "ВЫСОКИЙ"
    MIDDLE = "СРЕДНИЙ"
    LOW = "НИЗКИЙ"
    Priority = (
        (HIGH, "Высокий"),
        (MIDDLE, "Средний"),
        (LOW, "Низкий"),
    )

    NEW = "NEW"
    IN_WORK = "IN_WORK"
    FINISHED = "FINISHED"
    Status = (
        (NEW, "New"),
        (IN_WORK, "In_work"),
        (FINISHED, "Finished"),
    )

    title = models.CharField(max_length=200)
    students = models.ManyToManyField(Student, blank=True)
    description = models.TextField(blank=True)
    executor = models.ManyToManyField(Manager, blank=True)
    priority = models.CharField(max_length=9,
                              choices=Priority,
                              default=HIGH)
    date_added = models.DateTimeField(default=now,blank=True)
    date_finish = models.DateTimeField(default=now,blank=True)
    status = models.CharField(max_length=9,
                  choices=Status,
                  default=NEW)
    comment = models.TextField(blank=True)


    class Meta:
        verbose_name_plural = 'tasks'

    def __str__(self):
        return self.title


class KPI(models.Model):

    name = models.CharField(max_length=200)
    result = ArrayField(models.IntegerField())
    plan = ArrayField(models.IntegerField())
    year = models.IntegerField(default=2021)
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'kpi'

    def __str__(self):
        return self.name


class Finance(models.Model):

    INCOME = "Доход"
    EXPENSE = "Расход"
    PaymentType = (
        (INCOME, "Доход"),
        (EXPENSE, "Расход")
    )

    BANK = "Банковский счет"
    CARD = "Перевод на карту"
    ACQUIRING = "Эквайринг"
    TERMINAL = "Терминал"
    PFDO = "Сертификат ПФДО"
    PaymentAccount = (
        (BANK, "Банковский счет"),
        (CARD, "Перевод на карту"),
        (ACQUIRING, "Эквайринг"),
        (TERMINAL, "Терминал"),
        (PFDO, "Сертификат ПФДО"),
    )

    COURSES = "Курсы"
    CAMP = "Лагерь"
    RENT = "Аренда"
    SALARY = "Зарплата"
    ExpenseItem = (
        (COURSES, "Курсы"),
        (CAMP, "Лагерь"),
        (RENT, "Аренда"),
        (SALARY, "Зарплата"),
    )

    title = models.CharField(max_length=200)
    orderId = models.CharField(max_length=200, blank=True)
    payment_type = models.CharField(max_length=50, choices=PaymentType, default=INCOME)
    payment_account = models.CharField(max_length=50, choices=PaymentAccount, default=ACQUIRING)
    expense_item = models.CharField(max_length=50, choices=ExpenseItem, default=COURSES)
    amount = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=4, blank=True)
    payment_date = models.DateTimeField(default=now, blank=True)
    date_added = models.DateTimeField(default=now,blank=True)
    user_added = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Finances'

    def __str__(self):
        return self.title


#class Branch







