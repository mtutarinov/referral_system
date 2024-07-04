import datetime

import pytest
from .factories import UserFactory, ReferrerFactory, ReferralCodeFactory
from core.models import User, ReferralCode
from django.utils import timezone
import time


def test_verbose_name_field_user():
    assert User._meta.get_field('referrer').verbose_name == 'Реферер'
    assert User._meta.get_field('status').verbose_name == 'Статус пользователя'


def test_verbose_name_field_referral_code():
    assert ReferralCode._meta.get_field('name').verbose_name == 'Промокод'
    assert ReferralCode._meta.get_field('user').verbose_name == 'Владелец'
    assert ReferralCode._meta.get_field('is_active').verbose_name == 'Статус кода'
    assert ReferralCode._meta.get_field('create_date').verbose_name == 'Дата создания'


@pytest.mark.django_db
def test_save_method_referral_code(referral_code: ReferralCode):
    test_code = ReferralCodeFactory.create()
    pk = test_code.pk
    # У данного пользователя не существует активных кодов кроме указанного.
    assert not ReferralCode.objects.filter(is_active=True, user=test_code.user).exclude(pk=pk).exists()


@pytest.mark.django_db
def test_check_life_time_method_is_false_referral_code():
    test_code = ReferralCodeFactory.create()
    test_code.create_date -= datetime.timedelta(minutes=65)
    assert test_code.check_life_time() is False
    assert test_code.is_active is False


@pytest.mark.django_db
def test_check_life_time_method_is_true_referral_code():
    test_code = ReferralCodeFactory.create()
    test_code.create_date -= datetime.timedelta(minutes=30)
    assert test_code.check_life_time() is True
    assert test_code.is_active is True
