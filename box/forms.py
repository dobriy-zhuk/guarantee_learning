from django import forms
from .models import Lesson, Student


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = "__all__"

    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
