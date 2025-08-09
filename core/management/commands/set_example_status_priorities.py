from django.core.management.base import BaseCommand
from core.models import TicketStatus, TicketPriority


class Command(BaseCommand):
    help = "Seeds example ticket statuses and priorities."

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.NOTICE("Seeding example statuses and priorities...")
        )

        statuses = [
            {"name": "New", "weight": 1},
            {"name": "In Progress", "weight": 2},
            {"name": "Resolved", "weight": 3},
            {"name": "Closed", "weight": 4},
        ]

        priorities = [
            {"name": "Low", "weight": 1},
            {"name": "Medium", "weight": 2},
            {"name": "High", "weight": 3},
            {"name": "Critical", "weight": 4},
        ]

        for status in statuses:
            TicketStatus.objects.get_or_create(
                name=status["name"], defaults={"weight": status["weight"]}
            )

        for priority in priorities:
            TicketPriority.objects.get_or_create(
                name=priority["name"], defaults={"weight": priority["weight"]}
            )

        self.stdout.write(
            self.style.SUCCESS("Seeding example statuses and priorities completed")
        )
