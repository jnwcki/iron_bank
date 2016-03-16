from django.contrib.auth.forms import UserCreationForm
from django import forms


# Thinking of adding this to user creation form. not done yet

class NewUserCreation(UserCreationForm):
    account_name = forms.CharField()
