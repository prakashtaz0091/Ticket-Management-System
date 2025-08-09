from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import (
    MenuLevel1,
    MenuLevel2,
    MenuLevel3,
    Ticket,
    TicketPriority,
    TicketStatus,
    UserMenuAssignment,
)
from .permissions import (
    HasManagePriorityPermission,
    HasManageStatusPermission,
    HasMenuPermission,
    HasTicketPermission,
)
from .serializers import (
    MenuLevel1Serializer,
    MenuLevel2Serializer,
    MenuLevel3Serializer,
    TicketPrioritySerializer,
    TicketSerializer,
    TicketStatusSerializer,
    UserMenuAssignmentSerializer,
)
from .utils import has_permission


@api_view(["GET"])
def user_assigned_menus(request):
    user = request.user
    assignments = UserMenuAssignment.objects.filter(user=user)

    menu_level1_ids = assignments.values_list("menu_level1", flat=True).distinct()
    menu_level2_ids = assignments.values_list("menu_level2", flat=True).distinct()
    menu_level3_ids = assignments.values_list("menu_level3", flat=True).distinct()

    menus = {
        "menu_level1": MenuLevel1Serializer(
            MenuLevel1.objects.filter(id__in=menu_level1_ids), many=True
        ).data,
        "menu_level2": MenuLevel2Serializer(
            MenuLevel2.objects.filter(id__in=menu_level2_ids), many=True
        ).data,
        "menu_level3": MenuLevel3Serializer(
            MenuLevel3.objects.filter(id__in=menu_level3_ids), many=True
        ).data,
    }
    return Response(menus)


class UserMenuAssignmentViewSet(viewsets.ModelViewSet):
    queryset = UserMenuAssignment.objects.all()
    serializer_class = UserMenuAssignmentSerializer
    permission_classes = [HasMenuPermission]


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().select_related("menu_level3", "priority", "status")
    serializer_class = TicketSerializer
    permission_classes = [HasTicketPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        if has_permission(self.request.user, "can_view_all_tickets"):
            return queryset
        return queryset.filter(assigned_to=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TicketStatusViewSet(viewsets.ModelViewSet):
    queryset = TicketStatus.objects.all().order_by("weight")
    serializer_class = TicketStatusSerializer
    permission_classes = [HasManageStatusPermission]


class TicketPriorityViewSet(viewsets.ModelViewSet):
    queryset = TicketPriority.objects.all().order_by("weight")
    serializer_class = TicketPrioritySerializer
    permission_classes = [HasManagePriorityPermission]


class MenuLevel1ViewSet(viewsets.ModelViewSet):
    queryset = MenuLevel1.objects.all()
    serializer_class = MenuLevel1Serializer
    permission_classes = [HasMenuPermission]


class MenuLevel2ViewSet(viewsets.ModelViewSet):
    queryset = MenuLevel2.objects.all()
    serializer_class = MenuLevel2Serializer
    permission_classes = [HasMenuPermission]


class MenuLevel3ViewSet(viewsets.ModelViewSet):
    queryset = MenuLevel3.objects.all()
    serializer_class = MenuLevel3Serializer
    permission_classes = [HasMenuPermission]


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("core:dashboard")
        else:
            messages.error(request, "Invalid credentials")
            redirect("core:login")

    return render(request, "core/login.html")


def logout_view(request):
    logout(request)
    return redirect("core:login")


def dashboard(request):
    return render(request, "core/dashboard.html")
