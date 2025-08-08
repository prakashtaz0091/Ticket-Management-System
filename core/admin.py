from django.contrib import admin
from .models import *

admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(UserProfile)
admin.site.register(MenuLevel1)
admin.site.register(MenuLevel2)
admin.site.register(MenuLevel3)
admin.site.register(Ticket)
admin.site.register(TicketStatus)
admin.site.register(TicketPriority)