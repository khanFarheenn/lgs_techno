from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Request, Sponsor
import logging


logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def notify_sponsor_on_login(sender, request, user, **kwargs):
    
    logger.info(f"User {user.email} logged in, triggering the signal.")

    try:
        
        request_obj = Request.objects.get(user=user)
        logger.info(f"Found Request object for user {user.email}.")
        
        
        sponsor = Sponsor.objects.get(requestor=request_obj)
        logger.info(f"Found Sponsor for user {user.email}. Sending email...")

        
        send_mail(
            subject="Learner Login Notification",
            message=f"Dear {sponsor.requestor.user.first_name},\n\nThe learner with email {user.email} has logged in. Please review the approval status.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[sponsor.requestor.user.email],
        )
        logger.info(f"Email sent to sponsor: {sponsor.requestor.user.email}")

    except Request.DoesNotExist:
        logger.error(f"No request found for user: {user.email}")
    except Sponsor.DoesNotExist:
        logger.error(f"No sponsor found for the requestor: {user.email}")
