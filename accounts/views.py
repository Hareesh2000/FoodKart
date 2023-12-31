from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages,auth
from accounts.utils import check_role_customer, check_role_vendor, detectUser, send_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.tokens import default_token_generator
from order.models import Order
from restaurant.forms import RestaurantForm
from restaurant.models import Restaurant
from .models import User, UserProfile
from django.template.defaultfilters import slugify

from .forms import UserForm

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in!')
        return redirect('myAccount')
    elif request.method=='POST':
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
            mail_subject='Please activate your account'
            email_template='accounts/emails/account_verification_email.html'
            send_email(request,user,mail_subject,email_template)   
            messages.success(request,"Your account has created successfully!")
            return redirect('registerUser')
    else:
        form=UserForm()
    context={
        'form':form,
    }
    return render(request,'accounts/registerUser.html',context)

def registerRestaurant(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in!')
        return redirect('myAccount')
    elif request.method=='POST':
        user_form=UserForm(request.POST)
        res_form=RestaurantForm(request.POST,request.FILES)
        if user_form.is_valid() and res_form.is_valid() :
            first_name=user_form.cleaned_data['first_name']
            last_name=user_form.cleaned_data['last_name']
            username=user_form.cleaned_data['username']
            email=user_form.cleaned_data['email']
            password=user_form.cleaned_data['password']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.VENDOR
            user.save()
            res=res_form.save(commit=False)
            res.user=user
            restaurant_name=res_form.cleaned_data['restaurant_name']
            res.restaurant_slug=slugify(restaurant_name)+'-'+str(user.id)
            user_profile=UserProfile.objects.get(user=user)
            res.user_profile=user_profile
            res.save()
            mail_subject='Please activate your account'
            email_template='accounts/emails/account_verification_email.html'
            send_email(request,user,mail_subject,email_template)    
            messages.success(request,'Your request has been sent successfully! Please wait for the approval.')
        else:
            print('KeyErro')

    else:
        user_form=UserForm()
        res_form=RestaurantForm()

    context={
        'user_form':user_form,
        'res_form':res_form,
    }
    return render(request,'accounts/registerRestaurant.html',context)

def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)

    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"You have been activated!")
    else:
        messages.error(request,"Invalid activation link")
    
    return redirect('myAccount')

def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in!')
        return redirect('myAccount')
    elif request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"You have successfully logged in!")
            return redirect('myAccount')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('login')

    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,'You are logged out successfully')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user=request.user
    redirectUrl=detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    orders=Order.objects.filter(user=request.user,payment__isnull=False).order_by('-created_at')
    recent_orders=orders[:5]
    current_month_orders=Order.objects.filter(user=request.user,payment__isnull=False,created_at__month=datetime.now().month, created_at__year=datetime.now().year)

    context={
        'orders_count':orders.count(),
        'current_month_orders':current_month_orders,
        'recent_orders':recent_orders,
    }
    return render(request,'customer/custDashboard.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def restDashboard(request):
    restaurant=Restaurant.objects.get(user=request.user)
    orders=Order.objects.filter(restaurants__in=[restaurant.id],payment__isnull=False).order_by('-created_at')
    recent_orders=orders[:5]

    cur_month_orders=Order.objects.filter(restaurants__in=[restaurant.id],payment__isnull=False,
                         created_at__month=datetime.now().month,created_at__year=datetime.now().year)
    cur_month_revenue=0
    for order in cur_month_orders:
        cur_month_revenue+=order.get_total_by_restaurant()['total']

    total_revenue=0
    for order in orders:
        total_revenue+=order.get_total_by_restaurant()['total']
    context={
        'orders':orders,
        'orders_count':orders.count(),
        'recent_orders':recent_orders,
        'total_revenue':total_revenue,
        'cur_month_revenue':cur_month_revenue,
    }
    return render(request,'restaurant/restDashboard.html',context)

def forgot_password(request):
    if request.method=='POST':
        email=request.POST['email']

        if User.objects.filter(email=email).exists():
            user=User.objects.get(email__exact=email)
            mail_subject='Reset your password'
            email_template='accounts/emails/forgot_password_email.html'
            send_email(request,user,mail_subject,email_template)

            messages.success(request,'Password reset link has been sent to your email address')
            return redirect('login')
        else:
            messages.error(request,'Account doesn\'t exist')
            return redirect('login')

    return render(request,'accounts/forgot_password.html')

def reset_password_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)

    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.info(request,'Please set your password')
        return redirect('reset_password')
    else:
        messages.error(request,'This link has been expired')
        return redirect('myAccount') 


def reset_password(request):
    if request.method == 'POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if password==confirm_password:
            pk=request.session['uid']
            user=User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active=True
            user.save()
            messages.success(request,'Your password reset was successful')
            return redirect('login')
        else:
            messages.error('Passwords don\'t match')
            return redirect('reset_password')

    return render(request,'accounts/reset_password.html')