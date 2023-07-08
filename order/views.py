from django.http import HttpResponse, JsonResponse
import simplejson as json
from django.shortcuts import redirect, render
from accounts.models import UserProfile
from accounts.utils import send_notification
from foodKart_main.settings import RZP_KEY_ID, RZP_KEY_SECRET
from marketplace.context_processors import get_cart_totals
from marketplace.models import Cart

from order.forms import OrderForm
from django.contrib.auth.decorators import login_required

from order.models import Order, OrderedFood, Payment
from order.utils import generate_order_number

import razorpay

client = razorpay.Client(auth=(RZP_KEY_ID, RZP_KEY_SECRET))

@login_required(login_url='login')  
def checkout(request):
    cart_items=Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count=cart_items.count()

    if cart_count<=0:
        return redirect('marketplace')
    
    user_profile=UserProfile.objects.get(user=request.user)
    default_values={
        'first_name':request.user.first_name,
        'last_name':request.user.last_name,
        'phone':request.user.phone_number,
        'email':request.user.email,
        'address':user_profile.address,
        'state':user_profile.state,
        'city':user_profile.city,
        'pin_code':user_profile.pin_code,
    }
    form=OrderForm(initial=default_values)

    context={
        'form':form,
        'cart_items':cart_items,
    }
    return render(request,'order/checkout.html',context)

@login_required(login_url='login')
def place_order(request):

    cart_items=Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count=cart_items.count()

    if cart_count<=0:
        return redirect('marketplace')
    
    tax=get_cart_totals(request)['tax']   
    total=get_cart_totals(request)['total'] 
    tax_data=get_cart_totals(request)['tax_dict'] 
    
    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            order=Order()
            order.first_name=form.cleaned_data['first_name']
            order.last_name=form.cleaned_data['last_name']
            order.phone=form.cleaned_data['phone']
            order.email=form.cleaned_data['email']
            order.address=form.cleaned_data['address']
            order.state=form.cleaned_data['state']
            order.city=form.cleaned_data['city']
            order.pin_code=form.cleaned_data['pin_code']
            order.user=request.user
            order.total=total
            order.tax_data=json.dumps(tax_data)
            order.save()
            order.order_number = generate_order_number(order.id)
            order.save()

            DATA = {
                "amount": float(order.total) * 100,
                "currency": "INR",
                "receipt": "receipt #"+order.order_number,
                "notes": {
                    "key1": "value3",
                    "key2": "value2"
                    }
            }

            rzp_order=client.order.create(data=DATA)
            rzp_order_id=rzp_order['id']

            context={
                'order':order,
                'cart_items':cart_items,
                'rzp_order_id':rzp_order_id,
                'RZP_KEY_ID':RZP_KEY_ID,
                'rzp_amount': float(order.total) * 100,
            }
            return render(request,'order/place_order.html',context)
        
    return render(request,'order/place_order.html')

@login_required(login_url='login')
def payment(request):

   
    if request.headers.get('x-requested-with')=='XMLHttpRequest' and request.method=='POST':

         #storing payments in payment model
        order_number=request.POST.get('order_number')
        transaction_id=request.POST.get('transaction_id')
        status=request.POST.get('status')

        order=Order.objects.get(user=request.user,order_number=order_number)
        payment=Payment(
            user=request.user,
            transaction_id=transaction_id,
            amount=order.total,
            status=status,
        )
        payment.save()

        # updating order model
        order.payment=payment
        order.save()

        # moving ordered cart items to ordered food model
        cart_items=Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food=OrderedFood()
            ordered_food.order=order
            ordered_food.fooditem=item.fooditem
            ordered_food.quantity=item.quantity
            ordered_food.save()

        # sending order email to user

        mail_subject='Thank you for ordering with us.'
        mail_template='order/email/order_placed_email.html'

        context={
            'user':request.user,
            'order':order,
            'to_email':order.email,
        }

        send_notification(mail_subject,mail_template,context)

        # sending order email to restaurant
        
        mail_subject='You have received a new order.'
        mail_template='order/email/order_received_email.html'

        context={
            'user': cart_items[0].fooditem.restaurant.restaurant_name,
            'order':order,
            'to_email':cart_items[0].fooditem.restaurant.user.email,
        }

        send_notification(mail_subject,mail_template,context)

        # clearing cart
        cart_items.delete()
        
        response={
            'order_number': order_number,
            'transaction_id':transaction_id,
        }

        return JsonResponse(response)
    


def order_complete(request):
    order_number=request.GET.get('order_no')
    transaction_id=request.GET.get('trans_id')

    try:
        order=Order.objects.get(order_number=order_number,payment__transaction_id=transaction_id)
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
        return render(request,'order/order_complete.html',context)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return redirect('home')
    
                







