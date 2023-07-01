from django.conf import settings
from restaurant.models import Restaurant

def get_restaurant(request):
    try:
        restaurant=Restaurant.objects.get(user=request.user)
    except:
        restaurant=None
    return dict(restaurant=restaurant)

def get_google_api(request):
    return {'GOOGLE_API_KEY':settings.GOOGLE_API_KEY}