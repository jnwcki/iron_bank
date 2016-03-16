from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, DetailView, ListView

from bankapp.forms import NewUserCreation
from bankapp.models import Account, Transaction


class RestrictedAccessMixin:

    def get_queryset(self):
        return self.model.objects.filter(account__customer=self.request.user)


class IndexView(RestrictedAccessMixin, TemplateView):
    template_name = 'index.html'


class SignUp(CreateView):
    model = User
    form_class = NewUserCreation
    # Need to call a form_valid here to create the user's account

    def get_success_url(self):
        return reverse('login')


class ProfileView(RestrictedAccessMixin, ListView):
    # calls transaction_list.html
    model = Transaction


class TransactionView(RestrictedAccessMixin, CreateView):
    model = Transaction
    fields = ['amount', 'description', 'account', 'transaction_type',
              'destination_account_id'
              ]

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

