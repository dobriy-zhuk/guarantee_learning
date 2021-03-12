from django import forms
from .models import Lesson, Student, Manager, Teacher, Module, Subject, StudentStatus, Task, Finance, KPI, Branch
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from trumbowyg.widgets import TrumbowygWidget


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30, help_text='Username', widget=forms.TextInput(attrs={'placeholder': 'username'}))
    email = forms.EmailField(help_text='Ваш email')
    phone = forms.CharField(max_length=100, help_text='Ваш телефон')
    first_name = forms.CharField(max_length=100, help_text='Ваше имя')
    last_name = forms.CharField(max_length=100, help_text='Ваша фамилия')
    password1 = forms.CharField(widget=forms.PasswordInput, help_text='Придумайте пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, help_text='Повторите пароль')

    class Meta:
        model = User
        fields = ["username", "email", "phone", "first_name", "last_name", "password1", "password2"]


class UserForm(forms.ModelForm):

    username = forms.CharField(max_length=30, help_text='Имя пользователя')
    email = forms.EmailField(help_text='email пользователя')
    first_name = forms.CharField(max_length=100, help_text='Имя пользователя')
    last_name = forms.CharField(max_length=100, help_text='Фамилия пользователя')

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class StudentForm(forms.ModelForm):

    phone = forms.CharField(max_length=100, help_text='Телефон студента')
    status = forms.ModelChoiceField(queryset=StudentStatus.objects.all(),
                                     widget=forms.Select(attrs={'class': 'custom-select'}), help_text='Статус студента')

    class Meta:
        model = Student
        fields = ["phone", "status"]


class TeacherForm(forms.ModelForm):
    phone = forms.CharField(max_length=100, help_text='Телефон преподавателя')

    class Meta:
        model = Teacher
        fields = ["phone"]


class ManagerForm(forms.ModelForm):
    phone = forms.CharField(max_length=100, help_text='Телефон менеджера')

    class Meta:
        model = Manager
        fields = ["phone"]


class ModuleForm(forms.ModelForm):

    title = forms.CharField(max_length=100, help_text='Наименование модуля', widget=forms.Textarea(attrs={'class': 'col-12', 'rows': 1}))
    module_number = forms.IntegerField(help_text='Номер модуля в курсе')
    subject = forms.ModelChoiceField(help_text='Предмет', queryset=Subject.objects.all(), widget=forms.Select(attrs={'class': 'custom-select'}))
    student_text = forms.CharField(help_text='Контент студента', widget=forms.Textarea(attrs={'class': 'wysiwyg'}))
    teacher_text = forms.CharField(help_text='Контент учителя', widget=forms.Textarea(attrs={'class': 'wysiwyg'}))

    class Meta:
        model = Module
        fields = ["title", "module_number", "subject", "teacher_text", "student_text"]


class LessonForm(forms.ModelForm):

    name = forms.CharField(max_length=200, help_text='Наименование урока', widget=forms.Textarea(attrs={'class': 'col-12', 'rows': 1}))
    branch = forms.ModelChoiceField(help_text='Филиал', queryset=Branch.objects.all(), widget=forms.Select(attrs={'class': 'custom-select'}))
    subject = forms.ModelChoiceField(help_text='Предмет', queryset=Subject.objects.all(),
                                    widget=forms.Select(attrs={'class': 'custom-select'}))
    start = forms.DateTimeField(help_text='Старт занятия',
                                       widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M', attrs={'class':'datetimefield'}))
    teacher = forms.ModelMultipleChoiceField(
        queryset=Teacher.objects.all(),
        help_text='Учитель',
        widget=forms.SelectMultiple(attrs={'class': 'choices-1'})
    )
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        help_text='Студенты',
        widget=forms.SelectMultiple(attrs={'class': 'choices-10'})
    )

    duration = forms.IntegerField(help_text='Продолжительность, мин')

    class Meta:
        model = Lesson
        fields = ["name", "branch", "subject", "students", "teacher", "module","start", "duration"]


class KPIForm(forms.ModelForm):

    class Meta:
        model = KPI
        fields = "__all__"


class TaskForm(forms.ModelForm):

    title = forms.CharField(max_length=100, help_text='Наименование задачи', widget=forms.Textarea(attrs={'class': 'col-12', 'rows': 1}))
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        help_text='Привязанные ученики',
        widget=forms.SelectMultiple(attrs={'class': 'choices-10'})
    )
    description = forms.CharField(help_text='Описание задачи', widget=forms.Textarea(attrs={'class': 'wysiwyg'}))
    executor = forms.ModelMultipleChoiceField(
        queryset=Manager.objects.all(),
        help_text='Ответственный',
        widget=forms.SelectMultiple(attrs={'class': 'choices-1'})
    )
    priority = forms.ChoiceField(help_text='Приоритет', choices=Task.Priority, widget=forms.Select(attrs={'class': 'custom-select'}))
    status = forms.ChoiceField(help_text='Статус задачи', choices=Task.Status, widget=forms.Select(attrs={'class': 'custom-select'}))
    date_finish = forms.DateTimeField(help_text='Срок выполнения', widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'class':'datetimefield'}))
    comment = forms.CharField(max_length=100, help_text='Комментарий', widget=forms.Textarea)

    class Meta:
        model = Task
        fields = ["title", "students", "description","priority", "executor", "date_finish", "status", "comment"]



class FinanceForm(forms.ModelForm):

    title = forms.CharField(max_length=100, help_text='Наименование платежа', widget=forms.Textarea(attrs={'class': 'col-12', 'rows': 1}))
    payment_type = forms.ChoiceField(help_text='Тип платежа', choices=Finance.PaymentType, widget=forms.Select(attrs={'class': 'custom-select'}))
    payment_account = forms.ChoiceField(help_text='Счет платежа', choices=Finance.PaymentAccount, widget=forms.Select(attrs={'class': 'custom-select'}))
    expense_item = forms.ChoiceField(help_text='Статья платежа', choices=Finance.ExpenseItem,
                                        widget=forms.Select(attrs={'class': 'custom-select'}))
    amount = forms.IntegerField(help_text='Сумма платежа')
    payment_date = forms.DateTimeField(help_text='Дата платежа',
                                      widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'class':'datetimefield'}))
    user_added = forms.ModelChoiceField(queryset=User.objects.all(),
                                    widget=forms.Select(attrs={'class': 'custom-select'}), help_text='Кто оплатил?')
    comment = forms.CharField(max_length=100, help_text='Комментарий', widget=forms.Textarea)


    class Meta:
        model = Finance
        fields = ["title", "payment_type", "payment_account","expense_item", "amount", "payment_date", "user_added", "comment"]


class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = "__all__"

    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
