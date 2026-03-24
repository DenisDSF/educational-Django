from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm,
                                       PasswordChangeForm)
from django import forms

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class PersonalDataForm(forms.Form):
    name = forms.CharField(
        max_length=64,
        label='name',
        required=False,
        error_messages={
            'max_length': 'Имя должно быть не более 64 символов',
        }
    )
    surname = forms.CharField(
        max_length=64,
        label='password',
        required=False,
        error_messages={
            'max_length': 'Фамилия должна быть не более 64 символов',
        }
    )
    email = forms.EmailField(
        max_length=128,
        label='email',
        required=False,
        error_messages={
            'max_length': 'Почта должна быть не более 128 символов',
        }
    )


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='old_password',
        widget=forms.PasswordInput()
    )
    new_password1 = forms.CharField(
        label='new_password',
        widget=forms.PasswordInput()
    )
    new_password2 = forms.CharField(
        label='password_confirmation',
        widget=forms.PasswordInput()
    )