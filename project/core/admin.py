from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(User)
admin.site.register(ReferralCode)
admin.site.register(Profile)

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ['value']
