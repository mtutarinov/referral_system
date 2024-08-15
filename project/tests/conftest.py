import pytest
from pytest_factoryboy import register
from .factories import UserFactory, ReferrerFactory, ReferralCodeFactory, BalanceFactory, ProfileFactory
from django.urls import reverse
from rest_framework.test import APIClient

register(UserFactory)
register(ReferrerFactory)
register(ReferralCodeFactory)
register(BalanceFactory)


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


@pytest.fixture
def balance(user):
    return BalanceFactory.create(user=user)


@pytest.fixture
def balance_url():
    yield reverse('core:balance')


@pytest.fixture
def profile(user):
    return ProfileFactory(user=user)


@pytest.fixture
def profile_list_url():
    return reverse('core:profile-list')


@pytest.fixture
def profile_url(profile):
    return reverse('core:profile-detail', args=(profile.uuid,))


@pytest.fixture
def referral_register_url(referral_code):
    return f'/api/referral_register/{referral_code.uuid}/'
