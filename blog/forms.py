from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    title = forms.CharField(max_length=100, help_text='Наименование модуля')
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'wysiwyg'}), help_text='Текст урока')

    class Meta:
        model = Post
        fields = ["title", "text"]