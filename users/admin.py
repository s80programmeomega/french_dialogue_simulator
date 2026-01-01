from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Admin configuration for CustomUser model.
    Customizes the admin interface to work with email-based authentication.
    """

    # Fields to display in the user list
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "date_joined")

    # Fields for the user detail/edit page
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields for the add user page
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )

    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
