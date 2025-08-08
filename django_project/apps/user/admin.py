from django.contrib import admin
from allauth.account.models import EmailAddress
from .models import User

admin.site.unregister(EmailAddress)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'email', 'is_staff', 'is_active', 'groups')
