from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from restaurant.forms import RestaurantForm
from .models import User, UserProfile

from .forms import UserForm

# Create your views here.

def registerUser(request):
    if request.method=='POST':
        form=UserForm(request.POST)
        if form.is_valid():
            # user=form.save(commit=False)
            # user.role=User.CUSTOMER
            # user.save()
            # return redirect('registerUser')
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.CUSTOMER
            user.save()
            messages.success(request,"Yor account has been created successfully")
            return redirect('registerUser')
    else:
        form=UserForm()
    context={
        'form':form,
    }
    return render(request,'accounts/registerUser.html',context)

def registerRestaurant(request):
    if request.method=='POST':
        user_form=UserForm(request.POST)
        res_form=RestaurantForm(request.POST,request.FILES)
        if user_form.is_valid() and res_form.is_valid() :
            first_name=user_form.cleaned_data['first_name']
            last_name=user_form.cleaned_data['last_name']
            username=user_form.cleaned_data['username']
            email=user_form.cleaned_data['email']
            password=user_form.cleaned_data['password']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.RESTAURANT
            user.save()
            res=res_form.save(commit=False)
            res.user=user
            user_profile=UserProfile.objects.get(user=user)
            res.user_profile=user_profile
            res.save()
            messages.success(request,'Your request has been sent successfully! Please wait for the approval.')
        else:
            pass

    else:
        user_form=UserForm()
        res_form=RestaurantForm()

    context={
        'user_form':user_form,
        'res_form':res_form,
    }
    return render(request,'accounts/registerRestaurant.html',context)