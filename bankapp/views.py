from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, CreateView, DetailView, ListView, View, FormView
from django.views.generic.edit import ProcessFormView

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
        return render(request, 'bankapp/customer_list.html', {'profile': customer_profile,
                                                              'account': customer_account
                                                              }
                      )


class MoneyView(DetailView):
    model = Account

class TransferView(View):
    def get(self):
        pass
    def post(self):
        pass

class TransactionView(CreateView):
    template_name = 'bankapp/transaction_form.html'
    model = Transaction
    fields = ['amount', 'description', 'account', 'destination_account_id']
    """
    def post(self, form):
        to_acct = form.POST.get('to_acct')
        to_desc = form.POST.get('description')
        to_amt = (- form.POST.get('amount'))
        if to_acct:
            Transaction.objects.create(account_id=to_acct, description=to_desc, amount=to_amt)
        return super(TransactionView, self).post(self, **form)
    """
    def get_success_url(self):
        account_var = Account.objects.get(pk=self.kwargs['pk'])
        my_trans_variable = Transaction.objects.filter(account=account_var)
        add_money = 0

        for item in my_trans_variable:
            add_money += item.amount
        account_var.current_balance = add_money + account_var.beginning_balance
        account_var.save()
        return reverse('user_profile')


class TransactionDetailView(TemplateView):
    template_name = 'bankapp/transaction_detail.html'
    model = Transaction

    def get_context_data(self, **kwargs):
        context = super(TransactionDetailView, self).get_context_data(**kwargs)
        context['transaction_list'] = Transaction.objects.filter(account_id=kwargs['pk'])

        return context