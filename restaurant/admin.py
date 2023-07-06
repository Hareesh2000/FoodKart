from django.contrib import admin

from restaurant.models import OpeningHour, Restaurant

class RestaurantAdmin(admin.ModelAdmin):
    list_display=('restaurant_name','user','is_approved','created_at')
    list_display_links=('restaurant_name','user')

class OpeningHourAdmin(admin.ModelAdmin):
    list_display= ('restaurant','day','from_hour','to_hour')

admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(OpeningHour,OpeningHourAdmin)