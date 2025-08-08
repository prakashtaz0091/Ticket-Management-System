from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from .decorators import permission_required
from django.http import JsonResponse

from rest_framework import viewsets
from .models import MenuLevel1, MenuLevel2, MenuLevel3
from .serializers import MenuLevel1Serializer, MenuLevel2Serializer, MenuLevel3Serializer
from .utils import has_permission
from rest_framework.permissions import BasePermission
from .models import Ticket, TicketStatus, TicketPriority
from .serializers import TicketSerializer, TicketStatusSerializer, TicketPrioritySerializer


class HasTicketPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return has_permission(request.user, 'can_create_ticket')
        if view.action in ['update', 'partial_update']:
            return has_permission(request.user, 'can_edit_ticket')
        if view.action == 'destroy':
            return has_permission(request.user, 'can_delete_ticket')
        return has_permission(request.user, 'can_view_ticket')


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().select_related('menu_level3', 'priority', 'status')
    serializer_class = TicketSerializer
    permission_classes = [HasTicketPermission]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TicketStatusViewSet(viewsets.ModelViewSet):
    queryset = TicketStatus.objects.all().order_by('weight')
    serializer_class = TicketStatusSerializer
    permission_classes = [BasePermission]
    
    def has_permission(self, request, view):
        return has_permission(request.user, 'can_manage_status')


class TicketPriorityViewSet(viewsets.ModelViewSet):
    queryset = TicketPriority.objects.all().order_by('weight')
    serializer_class = TicketPrioritySerializer
    permission_classes = [BasePermission]
    
    def has_permission(self, request, view):
        return has_permission(request.user, 'can_manage_priority')
    


class HasMenuPermission(BasePermission):
    def has_permission(self, request, view):
        return has_permission(request.user, "can_manage_menus")


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


@permission_required('can_create_ticket')
def create_ticket_view(request):
    return JsonResponse({"message": "Ticket created (not really, just testing permission)"})



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
