from django import forms
from accounts.validators import image_validator

from restaurant.models import OpeningHour, Restaurant

class RestaurantForm(forms.ModelForm):
    restaurant_license=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[image_validator])
    class Meta:
        model=Restaurant
        fields = ['restaurant_name','restaurant_license']


class OpeningHourForm(forms.ModelForm):
    class Meta:
        model=OpeningHour
        fields = ['day','from_hour','to_hour','is_closed']
        
