from django.contrib.auth.models import User
from django.db import models


class Action(models.Model):
    resource = models.CharField(max_length=100)
    name = models.CharField(max_length=200)

    description = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ("resource", "name")

    def __str__(self):
        return f"{self.resource}:{self.name}"


class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    actions = models.ManyToManyField(Action, related_name="permissions")

    def __str__(self):
        return self.name

    @property
    def actions_list(self):
        if not hasattr(self, "__cached_actions_list"):
            self.__cached_actions_list = [
                f"{resource}:{name}"
                for resource, name in self.actions.values_list("resource", "name")
            ]
        return self.__cached_actions_list


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(Permission, related_name="roles")

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username


class MenuLevel1(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MenuLevel2(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        MenuLevel1, on_delete=models.CASCADE, related_name="children"
    )

    def __str__(self):
        return f"{self.parent.name} > {self.name}"


class MenuLevel3(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        MenuLevel2, on_delete=models.CASCADE, related_name="children"
    )

    def __str__(self):
        return f"{self.parent.parent.name} > {self.parent.name} > {self.name}"


class TicketStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "TicketStatus"


class TicketPriority(models.Model):
    name = models.CharField(max_length=100, unique=True)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "TicketPriorities"


class Ticket(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.ForeignKey(TicketStatus, on_delete=models.SET_NULL, null=True)
    priority = models.ForeignKey(TicketPriority, on_delete=models.SET_NULL, null=True)
    menu_level3 = models.ForeignKey(MenuLevel3, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_tickets"
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class UserMenuAssignment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="menu_assignments"
    )
    menu = models.ForeignKey(
        MenuLevel3, on_delete=models.CASCADE, related_name="menu_assignments"
    )

    class Meta:
        unique_together = ("user", "menu")

    def __str__(self):
        return f"{self.user.username} assigned to {self.menu}"


class NotificationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ticket = models.ForeignKey("Ticket", on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.ticket.title}"
