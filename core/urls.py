from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'menu-level1', MenuLevel1ViewSet)
router.register(r'menu-level2', MenuLevel2ViewSet)
router.register(r'menu-level3', MenuLevel3ViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'statuses', TicketStatusViewSet)
router.register(r'priorities', TicketPriorityViewSet)




app_name = "core"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('', dashboard, name='dashboard'),
    path("tickets/create/", create_ticket_view, name="create_ticket"),

] + router.urls