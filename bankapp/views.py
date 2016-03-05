from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, CreateView, DetailView, ListView, View, FormView

from bankapp.models import Customer, Account, AcctXref, Transaction


class RestrictedAccessMixin:
    def get_queryset(self):
        return self.model.objects.filter()


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        pass


class SignUp(CreateView):
    model = Customer
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('login')


class ProfileView(RestrictedAccessMixin, View):

    def get(self, request):
        customer_profile = Customer.objects.get(user=self.request.user)
        customer_account = Account.objects.filter(acctxref__customer=customer_profile)
        # customer_transaction = Transaction(account=customer_account)
        return render(request, 'bankapp/customer_list.html', {'profile': customer_profile,
                                                              'account': customer_account
                                                              }
                      )


class MoneyView(DetailView):
    model = Account


class TransactionView(CreateView):
    model = Transaction
    fields = ['amount', 'description', 'account']

    #def form_valid(self, form):
        # need logic to sum up transaction register and update account balance
        #trans = form.save(commit=False)
        #trans.save()
        #form.instance.account = Account.objects.get(self.kwargs['pk'])
        #pass
    def get_success_url(self):
        #print(self.kwargs)
        account_var = Account.objects.get(pk=self.kwargs['pk'])
        #my_cust_variable = Customer.objects.get(user=self.request.user)
        #my_trans_variable = Transaction.objects.filter(account__acctxref__customer=my_cust_variable)
        my_trans_variable = Transaction.objects.filter(account=account_var)
        add_money = 0

        for item in my_trans_variable:
            add_money += item.amount
        account_var.current_balance = add_money + account_var.beginning_balance
        account_var.save()
        #print(add_money)
        #print(account_var.current_balance)
        #print(my_trans_variable.values())
        return reverse('user_profile')
