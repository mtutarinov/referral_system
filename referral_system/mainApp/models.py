from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    referral_code = models.CharField(max_length=5, blank=True)
    referrer = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='referrals')
    # добавить статус юзера, чтобы при удалении, он деактивировался. Данные остаются у нас.


class ReferralCode(models.Model):
    name = models.CharField(max_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_codes')
    is_active = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.is_active:
            ReferralCode.objects.filter(is_active=True, user=self.user).update(is_active=False)
        super().save()

    def life_time(self):
        if timezone.now() - self.create_date >= timezone.timedelta(minutes=60):
            self.is_active = False
            self.save()
            return False
        else:
            return True
