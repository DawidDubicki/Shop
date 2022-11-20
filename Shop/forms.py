from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    email = forms.EmailField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'type': 'password',
                                                                                      'placeholder': 'Hasło'}))


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Wprowadż nazwę użytkownika'}))
    email = forms.EmailField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Wprowadź Email'}))
    password1 = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'type': 'password',
                                                                                      'placeholder': 'Wprowadź Hasło'}))
    password2 = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'type': 'password',
                                                                                      'placeholder': 'Powtórz Hasło'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', ]


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs=
                                                                         {'type': 'password',
                                                                          'placeholder': 'Wprowadź nowe hasło'}))
    new_password2 = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'type': 'password',
                                                                                 'placeholder': 'Powtórz nowe hasło'}))


class EmailChangeForm(forms.Form):
    new_email = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'type': 'email',
                                                                              'placeholder': 'Wprowadź nowy email'}))
    new_email2 = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'type': 'email',
                                                                               'placeholder': 'Powtórz nowy email'}))


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label='', max_length=100,  widget=forms.TextInput(attrs={'placeholder': 'email@gmail.com'}))
