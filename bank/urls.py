from django.urls import path
from .views import AccountCreateView
from django.views.generic import TemplateView

urlpatterns =[
    path("login",TemplateView.as_view(template_name="LogIn.html"),name="signin"),
    path("Register",AccountCreateView.as_view(),name="signup")
]
