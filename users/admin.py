from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # If you’ve added extra fields, you can customize fieldsets here
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("age", "can_be_contacted", "can_data_be_shared")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "age",
                    "can_be_contacted",
                    "can_data_be_shared",
                )
            },
        ),
    )
