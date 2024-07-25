from django.contrib import admin
from .models import CustomUser


admin.site.register(CustomUser)

# @admin.register(CustomUser)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ['id','username','first_name','last_name','date_of_birth','is_active','is_superuser','email','password']