

from restaurant.models import Restaurant


def get_restaurant(request):
    return Restaurant.objects.get(user=request.user)