from django.contrib import admin

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
admin.site.register(Action)
