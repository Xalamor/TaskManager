import django.forms

from .models import Task
from django.forms import ModelForm, TextInput, Textarea
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'task']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название'
        }),
            'task': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание'
        })}

class UserRegisterForm(UserCreationForm):
    email = django.forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя'
            }),
            'password': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите пароль'
            })}