from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form_input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form_input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form_input'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class AuthenticationUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form_input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form_input'}))

class SendOrder(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['city', 'street', 'house', 'apartment', 'number', 'firstname', 'lastname']

class QuantityProductForm(forms.ModelForm):
    class Meta:
        model = QuantityProduct
        fields = ['quantity']