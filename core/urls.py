from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    MenuLevel1ViewSet,
    MenuLevel2ViewSet,
    MenuLevel3ViewSet,
    TicketPriorityViewSet,
    TicketStatusViewSet,
    TicketViewSet,
    UserMenuAssignmentViewSet,
    dashboard,
    login_view,
    logout_view,
)

router = DefaultRouter()
router.register(r"menu-level1", MenuLevel1ViewSet, basename="menu-level1")
router.register(r"menu-level2", MenuLevel2ViewSet, basename="menu-level2")
router.register(r"menu-level3", MenuLevel3ViewSet, basename="menu-level3")
router.register(r"tickets", TicketViewSet, basename="ticket")
router.register(r"status", TicketStatusViewSet, basename="status")
router.register(r"priorities", TicketPriorityViewSet, basename="priorities")
router.register(
    r"user-menu-assignments",
    UserMenuAssignmentViewSet,
    basename="user-menu-assignments",
)


app_name = "core"

urlpatterns = [
    # template based
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("", dashboard, name="dashboard"),
] + router.urls
