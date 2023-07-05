from . import views
from django.urls import path


urlpatterns=[

    path('',views.marketplace,name='marketplace'),
    path('cart/',views.cart,name='cart'),
    path('cart/delete/<int:cartItem_id>',views.delete_cartItem,name='delete_cartItem'),

    path('add_to_cart/<int:food_id>/',views.add_to_cart,name="add_to_cart"),
    path('del_from_cart/<int:food_id>/',views.del_from_cart,name="del_from_cart"),

    path('<slug:restaurant_slug>/',views.restaurant_details,name='restaurant_details'),
]