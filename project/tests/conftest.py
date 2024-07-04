import pytest
from pytest_factoryboy import register
from .factories import UserFactory, ReferrerFactory, ReferralCodeFactory


@pytest.fixture
def referrer():
    yield ReferrerFactory.create()


@pytest.fixture
def user(referrer):
    yield UserFactory.create(referrer=referrer)


@pytest.fixture
def referral_code(user):
    yield ReferralCodeFactory.create(user=user)
