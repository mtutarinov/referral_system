from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from uuid import uuid4


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    referrer = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='referrals',
                                 verbose_name='Реферер')
    status = models.BooleanField(default=True, verbose_name='Статус пользователя')
    is_blogger = models.BooleanField(default=False, verbose_name='Блогер')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def soft_delete(self):
        self.objects.update(status=False)


class ReferralCode(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=5, verbose_name='Промокод')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_codes', verbose_name='Владелец')
    is_active = models.BooleanField(default=True, verbose_name='Статус кода')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', db_index=True)

    def save(self, *args, **kwargs):
        if self.is_active:
            # Можно ли оптимизировать?
            ReferralCode.objects.filter(is_active=True, user=self.user).update(is_active=False)
        super().save()

    def check_life_time(self):
        if timezone.now() - self.created_at >= timezone.timedelta(minutes=600):
            self.is_active = False
            self.save()
        return self.is_active


# пользователю сатус активности. Дополнительным методом.Сделать свой менеджер.
# Модель Профайл. И реализовать создание профайла через сигналы.

class Profile(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=150, verbose_name='Имя', null=True)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', null=True)
    age = models.IntegerField()
    telegram_profile = models.CharField(max_length=150, verbose_name='Профиль ТГ')
    telegram_channel = models.CharField(max_length=150, verbose_name='ТГ канал')
    telegram_subscribers = models.IntegerField(verbose_name='Подписчики в ТГ')
    youtube_profile = models.CharField(max_length=150, verbose_name='Пофиль в YouTube')
    youtube_channel = models.CharField(max_length=150, verbose_name='YouTube канал')
    youtube_subscribers = models.IntegerField(verbose_name='Подписчики в YouTube')
    status = models.BooleanField(default=True, verbose_name='Статус')
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь',
                                blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    balance = models.OneToOneField('Balance', on_delete=models.CASCADE, related_name='profile', verbose_name='Баланс')

class Balance(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    value = models.IntegerField(default=0, verbose_name='Баланс')
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='balance', verbose_name='Пользователь')
