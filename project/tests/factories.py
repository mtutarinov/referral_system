import factory
from faker import Faker

from django.db import models


from core.models import User, ReferralCode, Balance, Profile


class ReferrerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    uuid = factory.Faker('uuid4')
    username = factory.Faker('user_name')
    status = True
    is_blogger = True
    created_at = factory.Faker("date_time_this_decade", tzinfo=None)

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    uuid = factory.Faker('uuid4')
    referrer = factory.SubFactory(ReferrerFactory)
    username = factory.Faker('user_name')
    status = True
    is_blogger = False
    created_at = factory.Faker("date_time_this_decade", tzinfo=None)


class ReferralCodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReferralCode

    uuid = factory.Faker('uuid4')
    name = 'NNNN'
    user = factory.SubFactory(UserFactory)
    is_active = True
    created_at = factory.Faker("date_time_this_decade", tzinfo=None)

class BalanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Balance

    created_at = factory.Faker("date_time_this_decade", tzinfo=None)
    uuid = factory.Faker("uuid4")
    value = 0
    user = factory.SubFactory(UserFactory)

class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    uuid = factory.Faker('uuid4')
    first_name = factory.Faker("first_name_male", locale="ru_RU")
    last_name = factory.Faker("last_name_male", locale="ru_RU")
    age = 20
    telegram_profile = f'@{factory.Faker("user_name")}'
    telegram_channel = f'@{factory.Faker("user_name")}'
    telegram_subscribers = 100
    youtube_profile = factory.Faker("user_name")
    youtube_channel = factory.Faker("user_name")
    youtube_subscribers = 100
    status = True
    user = factory.SubFactory(UserFactory)
    created_at = factory.Faker("date_time_this_decade", tzinfo=None)
    balance = factory.SubFactory(BalanceFactory)