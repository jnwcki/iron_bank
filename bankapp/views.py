from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, CreateView, DetailView, ListView, View

from bankapp.models import Customer, Account, AcctXref


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
    pass
    def get(self, request):
         customer_profile = Customer.objects.get(user=self.request.user)
         customer_account = Account.objects.filter(acctxref__customer=customer_profile)
        #if self.request.user.id:
         #   user_urls = Url.objects.filter(user=self.request.user)
         return render(request, 'bankapp/customer_list.html', {'profile': customer_profile,
                                                               'account': customer_account
                                                               }
                       )