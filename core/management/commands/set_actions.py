from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Action


class Command(BaseCommand):
    help = "Sets actions which are core setup to link with permissions."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Setting up actions..."))

        # for viewset default actions
        resources = [
            "menu-level1",
            "menu-level2",
            "menu-level3",
            "ticket",
            "status",
            "priorities",
            "user-menu-assignments",
        ]
        actions = [
            "create",
            "list",
            "update",
            "destroy",
            "retrieve",
        ]

        # for custom actions on viewset
        custom_actions_resources = [
            ("get_assigned_menus", "user-menu-assignments"),
            ("get_assigned_tickets", "ticket"),
        ]

        for resource in resources:
            for action in actions:
                description = f"Helps to {action} {resource}"
                Action.objects.get_or_create(
                    name=action, resource=resource, description=description
                )

        for action, resource in custom_actions_resources:
            description = f"Helps to {action} from {resource}"
            Action.objects.get_or_create(
                name=action, resource=resource, description=description
            )

        self.stdout.write(self.style.SUCCESS("Actions setup completed."))
