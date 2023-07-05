from django.shortcuts import render
from foodKart_main.utils import get_current_location

from restaurant.models import Restaurant

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D 
from django.contrib.gis.db.models.functions import Distance


def home(request):
    if get_current_location(request) is not None:



        pnt=GEOSGeometry('POINT(%s %s)' % (get_current_location(request))   )
        restaurants=Restaurant.objects.filter(user_profile__location__distance_lte=(pnt,D(km=100))).annotate(distance=Distance("user_profile__location",pnt)).order_by("distance")
            
        for res in restaurants:
            res.dist=round(res.distance.km,1)
    else:
        restaurants=Restaurant.objects.filter(is_approved=True,user__is_active=True)[:8]

    context={
        'restaurants':restaurants,
    }
    return render(request,'home.html',context)