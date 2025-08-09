from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User

from .models import (
    Permission,
    Role,
    UserProfile,
    MenuLevel1,
    MenuLevel2,
    MenuLevel3,
    Ticket,
    TicketPriority,
    TicketStatus,
    UserMenuAssignment,
    NotificationLog,
    Action,
)


class TicketStatusAdmin(admin.ModelAdmin):
    list_display = ("name", "weight")


class TicketPriorityAdmin(admin.ModelAdmin):
    list_display = ("name", "weight")


class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "status",
        "priority",
        "menu_level3",
        "created_by",
        "assigned_to",
        "created_at",
        "updated_at",
    )


class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ["ticket", "user", "message", "created_at"]
    list_filter = ["user", "created_at"]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role"]


class ActionAdmin(admin.ModelAdmin):
    list_display = ["resource_name", "description"]
    search_fields = ["description"]

    def resource_name(self, obj):
        return f"{obj.name} : {obj.resource}"

    def has_add_permission(self, request):
        # Disable the Add button for everyone as actions are created automatically by the set_actions command
        return False

    def has_delete_permission(self, request, obj=None):
        # Disable the Delete button for everyone as actions are core part of the system
        return False

    def has_change_permission(self, request, obj=None):
        # Disable the Change button for everyone as actions are core part of the system, modifying will cause issues in permissions
        return False


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    # fk_name = "user"  # The OneToOneField in Profile to User


class CustomUserAdmin(DefaultUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        # Removed 'Permissions' fieldset completely
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )

    # Also remove filter_horizontal if it includes groups and user_permissions
    filter_horizontal = ()

    inlines = [UserProfileInline]


# Unregister the default User admin
admin.site.unregister(User)
# Register with your customized admin
admin.site.register(User, CustomUserAdmin)

admin.site.register(TicketStatus, TicketStatusAdmin)
admin.site.register(TicketPriority, TicketPriorityAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(UserMenuAssignment)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(MenuLevel1)
admin.site.register(MenuLevel2)
admin.site.register(MenuLevel3)
admin.site.register(NotificationLog, NotificationLogAdmin)
admin.site.register(Action, ActionAdmin)
