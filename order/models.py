import simplejson as json
from django.db import models

from accounts.models import User
from menu.models import FoodItem
from restaurant.models import Restaurant

request_object = ''

class Payment(models.Model):
   
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    restaurants=models.ManyToManyField(Restaurant,blank=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    tax_data = models.JSONField(blank=True, help_text = "Data format: {'tax_type':{'tax_percentage':'tax_amount'}}")
    total_data=models.JSONField(blank=True,null=True)
    total = models.FloatField()
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Concatenate first name and last name
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
    
    def order_placed_to(self):
        return ", ".join([str(i) for i in self.restaurants.all()])

    def get_total_by_restaurant(self):      
        restaurant=Restaurant.objects.get(user=request_object.user)
        total_data=json.loads(self.total_data)
        data=total_data.get(str(restaurant.id))

        subtotal=0
        tax=0
        tax_dict={}
        for key,val in data.items():
            subtotal+=float(key)
            val=val.replace("'",'"') # since for loads "" required
            val=json.loads(val)
            tax_dict.update(val) 

            for tax_perc in val:
                for tax_value in val[tax_perc]:
                    tax+=float(val[tax_perc][tax_value])   

        total=float(subtotal)+float(tax)

        context={
            'subtotal':subtotal,
            'tax_dict':tax_dict,
            'total':total,
        }
        return context

    def __str__(self):
        return self.order_number


class OrderedFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fooditem.food_name
