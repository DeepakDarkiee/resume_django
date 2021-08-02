from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib.auth.admin import UserAdmin


class UserInline(admin.TabularInline):
    model = User

class UserAdmin(admin.ModelAdmin):
  inlines = [UserInline,]
  list_display = ['username','account_approved']
    
admin.site.register(User, UserAdmin)
