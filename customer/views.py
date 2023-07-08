import simplejson as json
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.forms import UserInfoForm, UserProfileForm
from accounts.models import UserProfile

from accounts.utils import check_role_customer
from order.models import Order, OrderedFood



@login_required(login_url='login')
@user_passes_test(check_role_customer)
def profile(request):
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


def my_orders(request):
    orders=Order.objects.filter(user=request.user,payment__isnull=False).order_by('-created_at')

    context={
        'orders':orders,
    }

    return render(request,'customer/my_orders.html',context)\
    

def order_details(request,order_number):

    try:
        order=Order.objects.get(order_number=order_number,payment__isnull=False)
        ordered_foods=OrderedFood.objects.filter(order=order)

        subtotal=0
        for item in ordered_foods:
            subtotal+=(item.fooditem.price * item.quantity)

        tax_data=json.loads(order.tax_data)
        
        context={
             'order':order,
             'ordered_foods':ordered_foods,
             'subtotal':subtotal,
             'tax_data':tax_data,
        }
        return render(request,'customer/order_details.html',context)

    except:
        return redirect('customer')
    