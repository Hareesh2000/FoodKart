from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from marketplace.context_processors import get_cart_counter, get_cart_totals
from marketplace.models import Cart
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from restaurant.models import Restaurant
from django.contrib.auth.decorators import login_required


def marketplace(request):
    restaurants=Restaurant.objects.filter(is_approved=True,user__is_active=True)
    rest_count=restaurants.count()
    context={
        'restaurants':restaurants,
        'rest_count':rest_count,
    }
    return render(request,'marketplace/rest_list.html',context)

def restaurant_details(request,restaurant_slug):
    restaurant=get_object_or_404(Restaurant,restaurant_slug=restaurant_slug)
    categories=Category.objects.filter(restaurant=restaurant).prefetch_related( 
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
    else:
        cart_items=None
        
    context={
        'restaurant':restaurant,
        'categories':categories,
        'cart_items':cart_items,
    }
    return render(request,'marketplace/restaurant_details.html',context)


def add_to_cart(request,food_id):
    if request.user.is_authenticated:
        #checking if query is through ajax
        if request.headers.get('x-requested-with')=='XMLHttpRequest':
            #Check if food exists
            try:
                fooditem= FoodItem.objects.get(id=food_id)
                #Check if already food in cart 
                try:
                    chkCart=Cart.objects.get(user=request.user,fooditem=fooditem)
                    chkCart.quantity+=1
                    chkCart.save()  
                    return JsonResponse({'status':'Success','message':'Increased cart quantity','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_totals':get_cart_totals(request)})
                except:
                    chkCart=Cart.objects.create(user=request.user,fooditem=fooditem,quantity=1)
                    return JsonResponse({'status':'Success','message':'Added food to cart','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_totals':get_cart_totals(request)})
            except:
                return JsonResponse({'status':'Failed','message':'This food doesn\'t exists!'})
        else:
            return JsonResponse({'status':'Failed','message':'Invalid request!'})
    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue!'})
    

def del_from_cart(request,food_id):
    if request.user.is_authenticated:
        #checking if query is through ajax
        if request.headers.get('x-requested-with')=='XMLHttpRequest':
            #Check if food exists
            try:
                fooditem= FoodItem.objects.get(id=food_id)
                #Check if already food in cart 
                try:
                    chkCart=Cart.objects.get(user=request.user,fooditem=fooditem)
                    chkCart.quantity-=1
                    chkCart.save()
                    if chkCart.quantity==0:
                        chkCart.delete()  
                    return JsonResponse({'status':'Success','message':'Decreased cart quantity','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_totals':get_cart_totals(request)})
                except:
                    return JsonResponse({'status':'Failed','message':'No items to remove'})
            except:
                return JsonResponse({'status':'Failed','message':'This food doesn\'t exists!'})
        else:
            return JsonResponse({'status':'Failed','message':'Invalid request!'})
    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue!'})


@login_required(login_url='login')  
def cart(request):
    cart_items=Cart.objects.filter(user=request.user).order_by('created_at')


    context={
        'cart_items':cart_items,
    }
        
   
    return render(request,'marketplace/cart.html',context)   


def delete_cartItem(request,cartItem_id):
     if request.user.is_authenticated:  
        #checking if query is through ajax
        if request.headers.get('x-requested-with')=='XMLHttpRequest':
            #Check if cart item exists
            try:
                cart_item=Cart.objects.get(user=request.user,id=cartItem_id)
                cart_item.delete()
                return JsonResponse({'status':'Success','message':'Deleted cart item','cart_counter':get_cart_counter(request),'cart_totals':get_cart_totals(request)})
            except:
                return JsonResponse({'status':'Failed','message':'This Cart item doesn\'t exists!'})
            
        else:
            return JsonResponse({'status':'Failed','message':'Invalid request!'})

   