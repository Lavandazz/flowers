from django import forms
from django.contrib.auth.forms import AuthenticationForm

from users.models import User


class UserLoginForm(AuthenticationForm):
    """ Форма для входа зарегистрированного пользователя """
    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
