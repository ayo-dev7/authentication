from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class AccountManager(UserAdmin):
    list_display = ('email','username','first_name','last_name','last_login','is_active')
    list_display_links = ('email','username')
    readonly_fields = ('created_at','updated_at','last_login')
    
    fieldsets = ()
    filter_horizontal = ()
    list_filter = ()

admin.site.register(Account, AccountManager)
