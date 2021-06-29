from django.shortcuts import render,redirect

# Create your views here.
from .models import My_user,Transactions
from .forms import AccountCreationForm,LoginForm,TransactionForm
from django.views.generic import CreateView,TemplateView,ListView,View
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from .decorators import loginrequired
from django.utils.decorators import method_decorator
from .filters import TransactionFilter
from django.db.models import Q

class AccountCreateView(CreateView):
    model = My_user
    form_class = AccountCreationForm
    template_name = "AccountCreate.html"
    success_url = reverse_lazy("signin")

class SigninView(TemplateView):
    model = My_user
    form_class = LoginForm
    template_name = "Login.html"
    context = {}
    def get(self,request,*args, **kwargs):
        form = self.form_class()
        self.context["form"] = form
        return render(request,self.template_name,self.context)
    def post(self,request,*args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return redirect("home")
            else:
                print("Login failed")
            return render(request, self.template_name, self.context)


class Sign_out(View):
    def get(self,request):
        logout(request)
        return redirect("signin")



@method_decorator(loginrequired,name="dispatch")
class BalanceEnquiry(TemplateView):
    model = My_user
    template_name = "home.html"
    context = {}
    def get(self,request,*args,**kwargs):
        balance = request.user.balance
        print(balance)
        self.context["balance"]=balance
        return render(request, self.template_name, self.context)


class GetUserAccountMixin():
    def get_user_account(self,acc_no):
        try:
            return My_user.objects.get(account_number=acc_no)
        except:
            return None

@method_decorator(loginrequired,name="dispatch")
class FundTransfer(TemplateView,GetUserAccountMixin):
    model = Transactions
    template_name = 'FundTransfer.html'
    form_class = TransactionForm
    context={}
    def get(self,request, *args,**kwargs):
        self.context["form"] = self.form_class(initial={"from_account_number" : request.user.account_number})
        return render(request, self.template_name, self.context)
    def post(self,request, *args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            f_ac_no = request.user.account_number
            t_ac_no = form.cleaned_data["confirm_account_number"]
            amount = form.cleaned_data["amount"]
            nts = form.cleaned_data["notes"]
            transaction = Transactions(from_account_number=f_ac_no,
                                       to_account_number=t_ac_no,
                                       amount=amount,
                                       notes=nts)
            transaction.save()
            user = self.get_user_account(f_ac_no)
            user.balance-=amount
            user.save()
            user = self.get_user_account(t_ac_no)
            user.balance+=amount
            user.save()
            return redirect("home")

        else:
            form = self.form_class(request.POST)
            self.context["form"] = form
            return render(request, self.template_name, self.context)

@method_decorator(loginrequired,name="dispatch")
class PaymentHistory(TemplateView):
    model = Transactions
    template_name = "PaymentHistory.html"
    context={}
    def get(self,request, *args, **kwargs):
        c_transactions = self.model.objects.filter(to_account_number=request.user.account_number)
        d_transactions = self.model.objects.filter(from_account_number=request.user.account_number)
        self.context["c_transactions"] = c_transactions
        self.context["d_transactions"] = d_transactions
        return render(request, self.template_name, self.context)

@method_decorator(loginrequired,name="dispatch")
class TransactionFilterView(TemplateView):
    def get(self,request,*args,**kwargs):
        transactions = Transactions.objects.filter(Q(to_account_number=request.user.account_number) | Q(from_account_number=request.user.account_number))
        transaction_filter = TransactionFilter(request.GET,queryset=transactions)
        return render(request,"history.html",{'filter':transaction_filter})
