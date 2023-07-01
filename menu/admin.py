from django.contrib import admin

from menu.models import Category, FoodItem

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('category_name',)}
    list_display=('category_name','restaurant','modified_at')
    search_fields=('category_name','restaurant__restaurant_name')

class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('food_name',)}
    list_display=('food_name','category','restaurant','price','is_available','modified_at')
    search_fields=('food_name','category__category_name','restaurant__restaurant_name','price')
    list_filter=('is_available',)




admin.site.register(Category,CategoryAdmin)
admin.site.register(FoodItem,FoodItemAdmin)