from django.contrib import admin

from order.models import Order, OrderedFood, Payment


class OrderedFoodInline(admin.TabularInline):
    model=OrderedFood
    readonly_fields=('order','fooditem','quantity')
    extra=0

class OrderAdmin(admin.ModelAdmin):
    list_display=['order_number','name','phone','email','total','status','order_placed_to']
    inlines = [OrderedFoodInline]
    


admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderedFood)
