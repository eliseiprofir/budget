from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm

@admin.register(User)
class UserAdmin(UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ("email", "full_name", "is_active", "is_staff", "created", "last_login")
    list_filter = ("is_active", "is_staff", "is_superuser", "created")
    search_fields = ("email", "full_name")
    ordering = ("-created",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("full_name",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "created", "modified")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "password1", "password2"),
        }),
    )

    readonly_fields = ("created", "modified", "last_login")
