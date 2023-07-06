

from marketplace.models import Cart, Tax
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
    total_tax=0
    total=0
    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
        for item in cart_items:
            fooditem=FoodItem.objects.get(pk=item.fooditem.id)
            subtotal+=(fooditem.price * item.quantity)

    tax_dict={}
    taxes=Tax.objects.filter(is_active=True)
    for tax in taxes:
        tax_type=tax.tax_type           
        tax_percentage=tax.tax_percentage
        tax_amount=round((tax_percentage*subtotal)/100,2)
        total_tax+=tax_amount
        tax_dict.update({tax_type: {str(tax_percentage) : tax_amount}})

    total =subtotal+total_tax

    return dict(subtotal=subtotal,tax=total_tax,total=total,tax_dict=tax_dict)