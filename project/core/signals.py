from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User, ReferralCode, Profile, Balance


@receiver(post_save, sender=User)
def post_save_create_balance(sender, instance, created, **kwargs):
    if created:
        Balance.objects.create(user=instance)
