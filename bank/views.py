from django.shortcuts import render

# Create your views here.
from .models import My_user
from .forms import AccountCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy

class AccountCreateView(CreateView):
    model = My_user
    form_class = AccountCreationForm
    template_name = "AccountCreate.html"
    success_url = reverse_lazy("signin")