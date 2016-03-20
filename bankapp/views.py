from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, ListView
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
    template_name = 'bankapp/transaction_form.html'
    form_class = TransactionForm

    def get_form_kwargs(self):
            kwargs = super(TransactionView, self).get_form_kwargs()
            kwargs['user'] = self.request.user
            return kwargs

    def form_valid(self, form):
        new_transaction = form.save(commit=False)
        if new_transaction.transaction_type == 'W':
            if new_transaction.destination_account_id:
                return HttpResponseRedirect(reverse('invalid_transaction', kwargs={'error': '1'}))

        if new_transaction.transaction_type == 'D':
             if new_transaction.destination_account_id:
                return HttpResponseRedirect(reverse('invalid_transaction', kwargs={'error': '2'}))

        elif new_transaction.transaction_type == "T":
            if not new_transaction.destination_account_id:
                return HttpResponseRedirect(reverse('invalid_transaction', kwargs={'error': '3'}))

        account_var = Account.objects.get(customer=self.request.user)
        new_transaction.account = account_var
        trans_variable = Transaction.objects.filter(account=account_var)
        add_money = 0
        for item in trans_variable:
            add_money += item.amount

        if new_transaction.transaction_type == 'W':
            new_transaction.amount = -new_transaction.amount
        elif new_transaction.transaction_type == 'T':
            new_transaction.amount = -new_transaction.amount
            to_acct_add_money = 0
            to_acct_amts = Transaction.objects.filter(account=new_transaction.destination_account_id)

            for item in to_acct_amts:
                to_acct_add_money += item.amount
            to_acct_add_money -= new_transaction.amount
            # Create transfer on foreign account
            Transaction.objects.create(account=new_transaction.destination_account_id,
                                       amount=-new_transaction.amount,
                                       description=new_transaction.description,
                                       transaction_type='T',
                                       destination_account_id=account_var,
                                       new_balance=to_acct_add_money)

        new_transaction.new_balance = add_money + new_transaction.amount
        new_transaction.save()

        # Overdraft Fee
        if new_transaction.new_balance < 0:
            Transaction.objects.create(account=account_var,
                                       amount=-35,
                                       description="Overdraft Fee",
                                       transaction_type='F',
                                       new_balance=new_transaction.new_balance-35)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user_profile')


class InvalidView(TemplateView):
    template_name = 'invalid.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        error = self.kwargs.get('error')
        if error == '1':
            context['message'] = """You cannot withdraw from
                                    someone else's account"""
        elif error == '2':
            context['message'] = """You cannot deposit to someone else's account"""

        elif error == '3':
            context['message'] = """You must specify a destination account when
                                    selecting the transfer option"""
        return context
