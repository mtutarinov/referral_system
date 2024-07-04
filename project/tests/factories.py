import factory
from faker import Faker

# from core import models
from django.db import models
from core.models import User, ReferralCode


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
