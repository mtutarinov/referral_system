import pytest
from pytest_factoryboy import register
from .factories import UserFactory, ReferrerFactory, ReferralCodeFactory
from django.urls import reverse
from rest_framework.test import APIClient

register(UserFactory)
register(ReferrerFactory)
register(ReferralCodeFactory)


@pytest.fixture
def referrer():
    yield ReferrerFactory.create()


@pytest.fixture
def user(referrer):
    yield UserFactory.create(referrer=referrer)


@pytest.fixture
def referral_code(user):
    yield ReferralCodeFactory.create(user=user)


@pytest.fixture
def user_list_url():
    yield reverse('core:user-list')


@pytest.fixture
def user_url(user):
    yield reverse('core:user-detail', args=(user.id,))


@pytest.fixture
def referral_code_url(referral_code):
    yield reverse('core:referralcode-detail', args=(referral_code.uuid,))


@pytest.fixture
def referral_code_list_url():
    yield reverse('core:referralcode-list')


@pytest.fixture
def api_client():
    yield APIClient()
