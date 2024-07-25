import factory
from faker import Faker

from django.db import models
from core.models import User, ReferralCode, Balance, Profile


class ReferrerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    referrer = factory.SubFactory(ReferrerFactory)


class ReferralCodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReferralCode

    name = 'NNNN'
    is_active = True
    user = factory.SubFactory(UserFactory)


class BalanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Balance

    value = 0
    user = factory.SubFactory(UserFactory)


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    uuid = factory.Faker('uuid4')
    age = 20
    telegram_profile = f'@{factory.Faker("user_name")}'
    telegram_channel = f'@{factory.Faker("user_name")}'
    telegram_subscribers = 100
    youtube_profile = factory.Faker("user_name")
    youtube_channel = factory.Faker("user_name")
    youtube_subscribers = 100
    status = True
    user = factory.SubFactory(UserFactory)
