from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Seeds initial roles, permissions, users, menus, statuses, and priorities."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Seeding initial data..."))

        # setting up basic required actions
        call_command("set_actions")

        call_command("set_example_roles_users")

        call_command("set_example_status_priorities")

        self.stdout.write(self.style.SUCCESS("Seeding complete."))
