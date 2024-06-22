# authapp/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        subject = 'Compte super utilisateur créé'
        message = 'Vous avez été ajouté en tant que super utilisateur dans notre système.'
        from_email = settings.EMAIL_HOST_USER
        to_email = instance.email
        send_mail(subject, message, from_email, [to_email])
