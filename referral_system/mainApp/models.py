from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    referral_code = models.CharField(max_length=5, blank=True)
    referrer = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='referrals')


class ReferralCode(models.Model):
    name = models.CharField(max_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_codes')
    is_active = models.BooleanField(default=False)

