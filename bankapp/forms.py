from django.contrib.auth.forms import UserCreationForm
from django import forms
from bankapp.models import Transaction, Account


class NewUserCreation(UserCreationForm):
    account_name = forms.CharField()


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ['amount', 'description', 'transaction_type',
                  'destination_account_id']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['destination_account_id'].queryset = Account.objects.exclude(customer=user)
        self.fields['transaction_type'].choices = [('D', 'Deposit'),
                                                   ('W', 'Withdrawal'),
                                                   ('T', 'Transfer')
                                                   ]

