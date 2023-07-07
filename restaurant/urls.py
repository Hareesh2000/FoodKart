from django.urls import include, path
from . import views
from accounts import views as AccountViews


urlpatterns = [
    path('',AccountViews.restDashboard,name='restaurant'),
    path('rest_profile/',views.profile,name='rest_profile'),
    path('menu_builder/',include('menu.urls')),

    path('opening_hours/',views.opening_hours,name="opening_hours"),
    path('opening_hours/add',views.add_opening_hour,name="add_opening_hour"),
    path('opening_hours/delete/<int:pk>/',views.delete_opening_hour,name="delete_opening_hour"),   
    
]