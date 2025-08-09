from django.contrib import admin

from .models import *

admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(UserProfile)
admin.site.register(MenuLevel1)
admin.site.register(MenuLevel2)
admin.site.register(MenuLevel3)


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


admin.site.register(TicketStatus, TicketStatusAdmin)
admin.site.register(TicketPriority, TicketPriorityAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(UserMenuAssignment)


class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ["ticket", "user", "message", "created_at"]
    list_filter = ["user", "created_at"]


admin.site.register(NotificationLog, NotificationLogAdmin)
