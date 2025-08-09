from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Role


class Command(BaseCommand):
    help = "Seeds example users and roles."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Seeding example users and roles..."))

        # Use get_or_create to avoid duplicate unique constraint errors
        supervisor_role, _ = Role.objects.get_or_create(name="SupervisorRole")
        agent_role, _ = Role.objects.get_or_create(name="AgentRole")
        normal_role, _ = Role.objects.get_or_create(name="NormalRole")

        # Create superuser if not exists
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(username="admin", password="admin123")

        # Different types of users
        def create_user_if_not_exists(username, password, role):
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()
                user.profile.role = role
                user.profile.save()

        create_user_if_not_exists("supervisor", "supervisor123", supervisor_role)
        create_user_if_not_exists("agentuser", "agentuser123", agent_role)
        create_user_if_not_exists("normaluser", "normaluser123", normal_role)

        self.stdout.write(self.style.SUCCESS("Users and roles seeded."))
