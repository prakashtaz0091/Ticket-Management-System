from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import (
    Role, Permission, UserProfile,
    MenuLevel1, MenuLevel2, MenuLevel3,
    UserMenuAssignment,
    TicketStatus, TicketPriority
)

class Command(BaseCommand):
    help = "Seeds initial roles, permissions, users, menus, statuses, and priorities."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Seeding initial data..."))

        # Permissions
        perm_names = [
            'can_create_ticket',
            'can_edit_ticket',
            'can_view_all_tickets',
            'can_delete_ticket',
            'can_manage_status',
            'can_manage_priority',
            'can_manage_menus',
        ]
        permissions = []
        for name in perm_names:
            p, _ = Permission.objects.get_or_create(name=name)
            permissions.append(p)
        self.stdout.write(f"Created {len(permissions)} permissions")

        # Roles
        admin_role, _ = Role.objects.get_or_create(name='Admin')
        supervisor_role, _ = Role.objects.get_or_create(name='Supervisor')
        agent_role, _ = Role.objects.get_or_create(name='Agent')

        admin_role.permissions.set(permissions)
        supervisor_role.permissions.set(permissions[:5])  # fewer than admin
        agent_role.permissions.set(permissions[:3])  # create/edit/view ticket

        self.stdout.write("Roles created and permissions assigned")

        # Users
        admin_user, _ = User.objects.get_or_create(username='admin', email='admin@example.com')
        admin_user.set_password('admin123')
        admin_user.save()
        admin_user.userprofile.role = admin_role
        admin_user.userprofile.save()

        supervisor_user, _ = User.objects.get_or_create(username='supervisor', email='supervisor@example.com')
        supervisor_user.set_password('supervisor123')
        supervisor_user.save()
        supervisor_user.userprofile.role = supervisor_role
        supervisor_user.userprofile.save()

        agent_user, _ = User.objects.get_or_create(username='agent', email='agent@example.com')
        agent_user.set_password('agent123')
        agent_user.save()
        agent_user.userprofile.role = agent_role
        agent_user.userprofile.save()

        self.stdout.write("Sample users created")

        # Menu hierarchy
        dept_it = MenuLevel1.objects.create(name="IT")
        cat_hw = MenuLevel2.objects.create(name="Hardware", parent=dept_it)
        issue_bug = MenuLevel3.objects.create(name="Bug", parent=cat_hw)

        dept_hr = MenuLevel1.objects.create(name="HR")
        cat_payroll = MenuLevel2.objects.create(name="Payroll", parent=dept_hr)
        issue_delay = MenuLevel3.objects.create(name="Delay", parent=cat_payroll)

        self.stdout.write("Menu hierarchy created")

        # Assign menus to users
        UserMenuAssignment.objects.create(
            user=agent_user,
            menu_level1=dept_it,
            menu_level2=cat_hw,
            menu_level3=issue_bug
        )

        self.stdout.write("Menu assigned to agent user")

        # Statuses
        TicketStatus.objects.create(name="Open", weight=1)
        TicketStatus.objects.create(name="In Progress", weight=2)
        TicketStatus.objects.create(name="Closed", weight=3)

        # Priorities
        TicketPriority.objects.create(name="Low", weight=1)
        TicketPriority.objects.create(name="Medium", weight=2)
        TicketPriority.objects.create(name="High", weight=3)

        self.stdout.write("Statuses and priorities created")

        self.stdout.write(self.style.SUCCESS("Seeding complete."))
