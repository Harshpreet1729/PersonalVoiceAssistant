# users/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ""

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email')


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)
