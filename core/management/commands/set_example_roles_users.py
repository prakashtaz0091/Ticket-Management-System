from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Role


class Command(BaseCommand):
    help = "Seeds example users and roles."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Seeding example users and roles..."))

        # setting up basic example data to test

        # create few roles (Note: create whatever roles and permissions you need, with the help of admin panel by admin user)
        supervisor_role = Role.objects.create(name="SupervisorRole")
        agent_role = Role.objects.create(name="AgentRole")
        normal_role = Role.objects.create(name="NormalRole")

        # superuser to access admin panel
        User.objects.create_superuser(username="admin", password="admin123")

        # different types of users
        supervisor_user = User.objects.create_user(
            username="supervisor", password="supervisor123"
        )
        supervisor_user.profile.role = supervisor_role  # assign role
        supervisor_user.profile.save()

        agent_user = User.objects.create_user(
            username="agentuser", password="agentuser123"
        )
        agent_user.profile.role = agent_role  # assign role
        agent_user.profile.save()

        normal_user = User.objects.create_user(
            username="normaluser", password="normaluser123"
        )
        normal_user.profile.role = normal_role  # assign role
        normal_user.profile.save()

        self.stdout.write(self.style.SUCCESS("Users and roles seeded."))
