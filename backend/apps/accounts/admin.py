from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class FeedbackUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Public Profile",
            {
                "fields": (
                    "public_handle",
                    "auth_provider",
                    "provider_subject",
                    "gender",
                    "country_code",
                    "age_group",
                    "bio",
                )
            },
        ),
    )
    list_display = ("id", "username", "public_handle", "country_code", "age_group", "is_staff")
    search_fields = ("username", "public_handle", "email", "provider_subject")
