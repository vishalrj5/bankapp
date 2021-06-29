from django.urls import path
from .views import TransactionFilterView,Sign_out,AccountCreateView,SigninView,BalanceEnquiry,FundTransfer,PaymentHistory
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns =[
    path("login",SigninView.as_view(),name="signin"),
    path("Register",AccountCreateView.as_view(),name="signup"),
    path("home",login_required(TemplateView.as_view(template_name="home.html"),login_url="signin"),name="home"),
    path("balance",BalanceEnquiry.as_view(),name="balance"),
    path("transactions",FundTransfer.as_view(),name="transactions"),
    path("history",PaymentHistory.as_view(),name="history"),
    path("logout",Sign_out.as_view(),name="signout"),
    path("filterhistory",TransactionFilterView.as_view(),name="filterhistory"),

]
