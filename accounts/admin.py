from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):

    filter_horizontal=()
    list_filter=()
    fieldsets=()
    exclude=('date_joined','last_login',)
    
admin.site.register(User,CustomUserAdmin)
admin.site.register(UserProfile)