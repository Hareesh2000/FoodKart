from django import forms
from accounts.validators import image_validator

from restaurant.models import Restaurant

class RestaurantForm(forms.ModelForm):
    restaurant_license=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[image_validator])
    class Meta:
        model=Restaurant
        fields = ['restaurant_name','restaurant_license']
