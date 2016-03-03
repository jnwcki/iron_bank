from django.db import models

# Create your models here.
ACCOUNT_CHOICES = [('s', 'Savings'),
                   ('c', 'Checking')
                   ]


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_initial = models.CharField(max_length=1)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip_code = models.IntegerField()
    email = models.EmailField()


class Account(models.Model):
    account_type = models.CharField(max_length=30, choices=ACCOUNT_CHOICES)
    description = models.CharField(max_length=200)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2)
    beginning_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class AcctXref(models.Model):
    customer = models.ForeignKey(Customer)
    account = models.ForeignKey(Account)


class Transaction(models.Model):
    account = models.ForeignKey(Account)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)