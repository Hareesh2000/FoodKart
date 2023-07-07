from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.forms import UserInfoForm, UserProfileForm
from accounts.models import UserProfile

from accounts.utils import check_role_customer



@login_required(login_url='login')
@user_passes_test(check_role_customer)
def cust_profile(request):
    userProf=get_object_or_404(UserProfile,user=request.user)
    if request.method =='POST':
        profile_form= UserProfileForm(request.POST,request.FILES,instance=userProf)
        user_form=UserInfoForm(request.POST,instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request,'Your details have been updated successfully!')
            return redirect('cust_profile')

    else:
        profile_form= UserProfileForm(instance=userProf)
        user_form=UserInfoForm(instance=request.user)
    


    context={
        'userProf_form':profile_form,
        'user_form':user_form,
        'userProf':userProf,
    }
    return render(request,'customer/custProfile.html',context)
