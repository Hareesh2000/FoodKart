from django.contrib import admin

from restaurant.models import Restaurant

class RestaurantAdmin(admin.ModelAdmin):
    list_display=('restaurant_name','user','is_approved','created_at')
    list_display_links=('restaurant_name','user')



admin.site.register(Restaurant,RestaurantAdmin)