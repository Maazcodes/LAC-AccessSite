from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


from .models import AccessSiteCollection


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    readonly_fields = [
        "date_joined",
        "last_login",
    ]

    def get_fieldsets(self, request, obj=None):
        """Remove display of is_superuser and user_permissions fields for non-supers."""
        is_superuser = request.user.is_superuser
        if not is_superuser:
            self.fieldsets = (
                (None, {"fields": ("username", "password")}),
                (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
                (
                    _("Permissions"),
                    {
                        "fields": ("is_active", "is_staff", "groups"),
                    },
                ),
                (_("Important dates"), {"fields": ("last_login", "date_joined")}),
            )
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """Disable changing of is_superuser and user_permissions for non-superusers."""
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()

        if not is_superuser:
            disabled_fields |= {
                "is_superuser",
                "user_permissions",
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


admin.site.register(AccessSiteCollection)
