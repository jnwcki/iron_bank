from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, CreateView, DetailView

from bankapp.models import Customer


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


class ProfileView(RestrictedAccessMixin, DetailView):
    model = Customer