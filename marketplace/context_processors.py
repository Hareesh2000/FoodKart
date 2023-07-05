

from marketplace.models import Cart
from menu.models import FoodItem


def get_cart_counter(request):
    cart_count=0
    if request.user.is_authenticated:
        try:
            cart_items=Cart.objects.filter(user=request.user)
            for cart_item in cart_items:
                cart_count+=cart_item.quantity
 
        except:
            cart_count=0
    return dict(cart_count=cart_count)


def get_cart_totals(request):
    subtotal=0
    tax=0
    total=0
    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
        for item in cart_items:
            fooditem=FoodItem.objects.get(pk=item.fooditem.id)
            subtotal+=(fooditem.price * item.quantity)

        total=subtotal+tax
    print(total)
    print(subtotal)
    return dict(subtotal=subtotal,tax=tax,total=total)