from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.utils import check_role_vendor
from menu.models import Category, FoodItem
from restaurant.models import Restaurant
from .forms import RestaurantForm
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





