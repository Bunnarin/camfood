from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.db.models import Q
from allauth.account.models import EmailAddress
from .models import User

admin.site.unregister(EmailAddress)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'email', 'is_staff', 'is_active', 'groups')

admin.site.unregister(Group)
@admin.register(Group)
class CustomGroupAdmin(admin.ModelAdmin):
    """  
    This admin class extends the default Group admin to provide:
    - Permission filtering based on user's own permissions to ensure SECURITY
    - Extended permissions for users with faculty-wide or global access
    """

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        """
        this just does some logic and modify the kwargs before passing it to the super
        """
        if db_field.name == "permissions":
            if request and not request.user.is_superuser:
                user = request.user
                available_perms = Permission.objects.filter(group__in=user.groups.all()).distinct()
                kwargs["queryset"] = available_perms.select_related("content_type")
            else:
                kwargs["queryset"] = Permission.objects.all().select_related("content_type")

        return super().formfield_for_manytomany(db_field, request=request, **kwargs)
