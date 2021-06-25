from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import My_user


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = My_user
        fields = ["first_name", "username", "email", "password1","password2","account_number",
                  "account_type","balance","phone"]