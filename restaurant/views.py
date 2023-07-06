from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from accounts.context_processors import get_restaurant
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.utils import check_role_vendor
from menu.models import Category, FoodItem
from restaurant.models import OpeningHour, Restaurant
from .forms import OpeningHourForm, RestaurantForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def profile(request):
    userProf=get_object_or_404(UserProfile,user=request.user)
    rest=get_object_or_404(Restaurant,user=request.user)
    if request.method=='POST':
        userProf_form=UserProfileForm(request.POST,request.FILES,instance=userProf)
        rest_form=RestaurantForm(request.POST,request.FILES,instance=rest)
        if userProf_form.is_valid() and rest_form.is_valid():
            userProf_form.save()
            rest_form.save()
            messages.success(request,'Restaurant details updated successfully!')
            return redirect('profile')

    else:
        userProf_form=UserProfileForm(instance=userProf)
        rest_form=RestaurantForm(instance=rest)

    context={
        'userProf':userProf,
        'rest':rest,
        'userProf_form':userProf_form,
        'rest_form':rest_form,
    }
    return render(request,'restaurant/restProfile.html',context)



def opening_hours(request):
    opening_hours=OpeningHour.objects.filter(restaurant=get_restaurant(request)['restaurant'])
    form=OpeningHourForm()
    context={
        'form':form,
        'opening_hours':opening_hours,
    }

    return render(request,'restaurant/opening_hours.html',context)


def add_opening_hour(request):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with')== 'XMLHttpRequest' and request.method== 'POST':
            day=request.POST.get('day')
            from_hour=request.POST.get('from_hour')
            to_hour=request.POST.get('to_hour')
            is_closed=request.POST.get('is_closed')

            try:
                hour=OpeningHour.objects.create(restaurant=get_restaurant(request)['restaurant'],day=day,from_hour=from_hour,to_hour=to_hour,is_closed=is_closed)
                day=OpeningHour.objects.get(id=hour.id)
                response={'status':'success','id':hour.id,'day': day.get_day_display(),'from_hour':from_hour,'to_hour':to_hour,'is_closed':is_closed}
            except IntegrityError as e:
                response={'status':'failed','message':from_hour+'-'+to_hour+ ' already exists for this day!'}
            return JsonResponse(response)
        else:
            return HttpResponse("Invalid Request")


def delete_opening_hour(request,pk=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with')== 'XMLHttpRequest':
            hour=get_object_or_404(OpeningHour,pk=pk)
            hour.delete()
            response={'status':'success','id':pk}
            
        else:
            response={'status':'failed'}
        
        return JsonResponse(response)
    

