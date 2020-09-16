from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
    username=forms.CharField(label='姓名',max_length=20)
    password=forms.CharField(label='密碼',widget=forms.PasswordInput())

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")