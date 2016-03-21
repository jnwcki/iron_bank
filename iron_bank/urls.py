"""iron_bank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from bankapp.views import IndexView, ProfileView, TransactionView, SignUp, InvalidView, \
    TransactionDetailView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^accounts/login/', auth_views.login, name='login'),
    url(r'^logout/', auth_views.logout_then_login, name='logout'),
    url(r'^account/profile/', ProfileView.as_view(), name='user_profile'),
    url(r'^account/transactions/$', TransactionView.as_view(), name='transaction'),
    url(r'^signup/', SignUp.as_view(), name='signup'),
    url(r'^invalid/(?P<error>\d+)', InvalidView.as_view(), name='invalid_transaction'),
    url(r'^transaction/detail/(?P<pk>\d+)', TransactionDetailView.as_view(), name='trans_detail')
]
