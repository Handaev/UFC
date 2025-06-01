from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser

input_form = 'form-control w-100 py-2 px-3 border rounded-md shadow-sm'


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'placeholder': 'Your username',
            'class': input_form
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password',
            'class': input_form
        })
    )


class SignupForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'placeholder': 'Your username',
            'class': input_form
        })
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your email address',
            'class': input_form
        })
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password',
            'class': input_form
        })
    )

    password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password',
            'class': input_form
        })
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(UserChangeForm):
    password = None  # Убираем поле смены пароля

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'is_fighter', 'is_manager']
        widgets = {
            'is_fighter': forms.CheckboxInput(),
            'is_manager': forms.CheckboxInput(),
        }