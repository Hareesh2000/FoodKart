from django.shortcuts import render

from restaurant.models import Restaurant


def home(request):
    restaurants=Restaurant.objects.filter(is_approved=True,user__is_active=True)[:8]

    context={
        'restaurants':restaurants,
    }
    return render(request,'home.html',context)