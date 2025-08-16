# events/signals.py
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Event

@receiver(m2m_changed, sender=Event.participants.through)
def send_rsvp_email(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            user = instance.participants.get(pk=user_id)
            send_mail(
                subject=f"RSVP Confirmation for {instance.name}",
                message=f"Hi {user.username},\n\nYou have successfully RSVP'd for {instance.name} on {instance.date}.",
                from_email="noreply@example.com",
                recipient_list=[user.email],
                fail_silently=False,
            )
