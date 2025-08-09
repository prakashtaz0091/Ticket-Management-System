from rest_framework import serializers
from .models import (
    MenuLevel1,
    MenuLevel2,
    MenuLevel3,
    TicketStatus,
    TicketPriority,
    Ticket,
    UserMenuAssignment,
)


class UserMenuAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMenuAssignment
        fields = "__all__"


class MenuLevel1Serializer(serializers.ModelSerializer):
    class Meta:
        model = MenuLevel1
        fields = "__all__"


class MenuLevel2Serializer(serializers.ModelSerializer):
    class Meta:
        model = MenuLevel2
        fields = "__all__"


class MenuLevel3Serializer(serializers.ModelSerializer):
    class Meta:
        model = MenuLevel3
        fields = "__all__"


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatus
        fields = "__all__"


class TicketPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPriority
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Ticket
        fields = "__all__"
