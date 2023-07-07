from django.urls import include, path
from . import views
from accounts import views as AccountViews


urlpatterns = [
    path('',AccountViews.custDashboard,name='customer'),
    path('cust_profile/',views.cust_profile,name='cust_profile'),
]