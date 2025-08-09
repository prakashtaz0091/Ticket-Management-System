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
from .permissions import RoleBasedPermission

from .serializers import (
    MenuLevel1Serializer,
    MenuLevel2Serializer,
    MenuLevel3Serializer,
    TicketPrioritySerializer,
    TicketSerializer,
    TicketStatusSerializer,
    UserMenuAssignmentSerializer,
)
from rest_framework.decorators import action


class UserMenuAssignmentViewSet(viewsets.ModelViewSet):
    queryset = UserMenuAssignment.objects.all()
    serializer_class = UserMenuAssignmentSerializer
    permission_classes = [RoleBasedPermission]

    @action(detail=False, methods=["get"], url_path="get-assigned-menus")
    def get_assigned_menus(self, request):
        user = request.user
        assigned_menus = UserMenuAssignment.objects.filter(user=user)
        serializer = UserMenuAssignmentSerializer(assigned_menus, many=True)
        return Response(serializer.data)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().select_related("menu_level3", "priority", "status")
    serializer_class = TicketSerializer
    permission_classes = [RoleBasedPermission]

    @action(detail=False, methods=["get"], url_path="get-assigned-tickets")
    def get_assigned_tickets(self, request):
        user = request.user
        assigned_tickets = Ticket.objects.filter(assigned_to=user)
        serializer = TicketSerializer(assigned_tickets, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TicketStatusViewSet(viewsets.ModelViewSet):
    queryset = TicketStatus.objects.all().order_by("weight")
    serializer_class = TicketStatusSerializer
    permission_classes = [RoleBasedPermission]


class TicketPriorityViewSet(viewsets.ModelViewSet):
    queryset = TicketPriority.objects.all().order_by("weight")
    serializer_class = TicketPrioritySerializer
    permission_classes = [RoleBasedPermission]


class MenuLevel1ViewSet(viewsets.ModelViewSet):
    queryset = MenuLevel1.objects.all()
    serializer_class = MenuLevel1Serializer
    permission_classes = [RoleBasedPermission]


class MenuLevel2ViewSet(viewsets.ModelViewSet):
    queryset = MenuLevel2.objects.all()
    serializer_class = MenuLevel2Serializer
    permission_classes = [RoleBasedPermission]


class MenuLevel3ViewSet(viewsets.ModelViewSet):
    queryset = MenuLevel3.objects.all()
    serializer_class = MenuLevel3Serializer
    permission_classes = [RoleBasedPermission]


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
