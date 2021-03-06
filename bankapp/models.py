from django.db import models
from django.contrib.auth.models import User

TRANS_TYPES = [('D', 'Deposit'),
               ('W', 'Withdrawal'),
               ('T', 'Transfer'),
               ('F', 'Bank Fee')
               ]


class Account(models.Model):
    customer = models.OneToOneField("auth.User")
    account_name = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.account_name)


class Transaction(models.Model):
    account = models.ForeignKey(Account, related_name='from_account')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    destination_account_id = models.IntegerField(null=True, blank=True)
    transaction_time = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=15, choices=TRANS_TYPES)
    new_balance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["-transaction_time"]

    def __str__(self):
        return "{} {}".format(self.description, self.amount)