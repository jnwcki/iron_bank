from django.contrib import admin

# Register your models here.
from bankapp.models import Customer, Account, AcctXref, Transaction

admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(AcctXref)
admin.site.register(Transaction)