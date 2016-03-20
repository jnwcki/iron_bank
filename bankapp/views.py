from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, DetailView, ListView

from bankapp.forms import NewUserCreation, TransactionForm
from bankapp.models import Account, Transaction


class RestrictedAccessMixin:

    def get_queryset(self):
        return self.model.objects.filter(account__customer=self.request.user)


class IndexView(TemplateView):
    template_name = 'index.html'


class SignUp(CreateView):
    model = User
    form_class = NewUserCreation

    def form_valid(self, form):
        user_form = form.save()
        new_account_name = form.cleaned_data.get('account_name')
        Account.objects.create(account_name=new_account_name, customer=user_form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('login')


class ProfileView(RestrictedAccessMixin, ListView):
    # calls transaction_list.html
    model = Transaction


class TransactionView(CreateView):
    # model = Transaction
    template_name = 'bankapp/transaction_form.html'
    form_class = TransactionForm

    def get_form_kwargs(self):
            kwargs = super(TransactionView, self).get_form_kwargs()
            kwargs['user'] = self.request.user
            return kwargs


    #def form_valid(self, form):
        #new_trans = form.save()
           # Transaction.objects.create(account_id=to_acct, description=to_desc, amount=to_amt)
        #return super(TransactionView, self)

    def get_success_url(self):
        """
        account_var = Account.objects.get(pk=self.kwargs['pk'])
        my_trans_variable = Transaction.objects.filter(account=account_var)
        add_money = 0

        for item in my_trans_variable:
            add_money += item.amount
        account_var.current_balance = add_money + account_var.beginning_balance
        account_var.save()
        """
        return reverse('user_profile')

