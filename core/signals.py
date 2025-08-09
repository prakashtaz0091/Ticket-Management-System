from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Ticket, NotificationLog


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=Ticket)
def ticket_created_or_updated(sender, instance, created, **kwargs):
    user = instance.created_by
    ticket = instance

    if created:
        msg = f"Ticket '{ticket.title}' was created by {user.username}."
    else:
        msg = f"Ticket '{ticket.title}' was updated by {user.username}."

    # Log to console
    print("[NOTIFICATION]", msg)

    # Save to DB
    NotificationLog.objects.create(user=user, ticket=ticket, message=msg)


@receiver(pre_save, sender=Ticket)
def ticket_assignment_changed(sender, instance, **kwargs):
    if not instance.pk:
        return  # Skip if this is a new object (handled in post_save)

    previous = Ticket.objects.get(pk=instance.pk)
    if previous.assigned_to != instance.assigned_to:
        msg = f"Ticket '{instance.title}' was reassigned to {instance.assigned_to.username if instance.assigned_to else 'nobody'}."
        print("[NOTIFICATION]", msg)

        NotificationLog.objects.create(
            user=instance.assigned_to, ticket=instance, message=msg
        )
