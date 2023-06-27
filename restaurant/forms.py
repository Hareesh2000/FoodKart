from django import forms

from restaurant.models import Restaurant

class RestaurantForm(forms.ModelForm):
    class Meta:
        model=Restaurant
        fields = ['restaurant_name','restaurant_license']
