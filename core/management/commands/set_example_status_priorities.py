from django.core.management.base import BaseCommand
from core.models import TicketStatus, TicketPriority


class Command(BaseCommand):
    help = "Seeds example ticket statuses and priorities."

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.NOTICE("Seeding example statuses and priorities...")
        )

        # setting up basic example data to test
        TicketStatus.objects.bulk_create(
            [
                TicketStatus(name="New", weight=1),
                TicketStatus(name="In Progress", weight=2),
                TicketStatus(name="Resolved", weight=3),
                TicketStatus(name="Closed", weight=4),
            ]
        )

        TicketPriority.objects.bulk_create(
            [
                TicketPriority(name="Low", weight=1),
                TicketPriority(name="Medium", weight=2),
                TicketPriority(name="High", weight=3),
                TicketPriority(name="Critical", weight=4),
            ]
        )

        self.stdout.write(
            self.style.SUCCESS("Seeding example statuses and priorities completed")
        )
