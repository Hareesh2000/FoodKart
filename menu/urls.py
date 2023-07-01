from django.urls import path

from menu import views


urlpatterns=[
    path('',views.menu_builder,name='menu_builder'),
    path('category/<int:pk>/',views.fooditems_by_category,name='fooditems_by_category'),
    path('category/add/',views.add_category,name='add_category'),
    path('category/edit/<int:pk>/',views.edit_category,name='edit_category'),
    path('category/delete/<int:pk>/',views.delete_category,name='delete_category'),
]