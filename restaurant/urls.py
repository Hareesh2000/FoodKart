from django.urls import include, path
from . import views
from accounts import views as AccountViews


urlpatterns = [
    path('',AccountViews.restDashboard,name='restaurant'),
    path('profile/',views.profile,name='profile'),
    path('menu_builder/',include('menu.urls')),
    
]