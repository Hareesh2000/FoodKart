from django.urls import include, path
from . import views
from accounts import views as AccountViews


urlpatterns = [
    path('',AccountViews.custDashboard,name='customer'),
    path('profile/',views.profile,name='cust_profile'),
    path('my_orders/',views.my_orders,name='customer_orders'),
    path('order_details/<int:order_number>/',views.order_details ,name='order_details'),
]