from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Task

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "name", "role", "is_active", "is_deleted")
    list_filter = ("role", "is_active", "is_deleted")
    ordering = ("email",)
    search_fields = ("email", "name")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("name", "phone", "bio")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Role", {"fields": ("role",)}),
        ("Soft Delete", {"fields": ("is_deleted", "deleted_at")}),
        ("Important Dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "role", "password1", "password2"),
            },
        ),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "priority",
        "creator",
        "assigned_to",
        "is_deleted",
    )
    list_filter = ("status", "priority", "is_deleted")
    search_fields = ("title",)
