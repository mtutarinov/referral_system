import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import User, ReferralCode, Balance, Profile
from .factories import UserFactory, ReferrerFactory, ReferralCodeFactory

from datetime import datetime


# Тесты для User.
@pytest.mark.django_db
def test_user_list(user_list_url: str, api_client: APIClient, user: User):
    response = api_client.get(user_list_url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == User.objects.count()
    # Добавить анонимуса


@pytest.mark.django_db
def test_user_detail(user_url: str, api_client: APIClient, user: User):
    response = api_client.get(user_url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 8
    assert 'id' not in response.data
    assert response.data['uuid'] == str(user.uuid)
    assert response.data['referrer'] == user.referrer.username
    assert response.data['username'] == user.username
    assert response.data['first_name'] == user.first_name
    assert response.data['last_name'] == user.last_name
    assert response.data['email'] == user.email
    assert response.data['status'] == user.status
    assert response.data['is_blogger'] == user.is_blogger


# Тесты для ReferralCode.
@pytest.mark.django_db
def test_referral_code_get_authorized(referral_code_url: str, api_client: APIClient, referral_code: ReferralCode,
                                      user: User):
    api_client.force_authenticate(user)
    response = api_client.get(referral_code_url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5
    assert response.data['uuid'] == str(referral_code.uuid)
    assert response.data['name'] == referral_code.name
    assert response.data['user'] == referral_code.user.username
    assert datetime.strptime(response.data['create_date'],
                             "%Y-%m-%dT%H:%M:%S.%fZ") == referral_code.create_date.replace(tzinfo=None)
    assert response.data['is_active'] == referral_code.is_active
    assert 'id' not in response.data


@pytest.mark.django_db
def test_referral_code_get_unauthorized(referral_code_url: str, api_client: APIClient, referral_code: ReferralCode,
                                        user: User):
    response = api_client.get(referral_code_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_referral_code_post_authorized(referral_code_list_url: str, api_client: APIClient, user: User):
    api_client.force_authenticate(user)
    data = {
        'name': 'code',
        'is_active': True
    }
    response = api_client.post(referral_code_list_url, data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['user'] == user.username


@pytest.mark.django_db
def test_referral_code_post_unauthorized(referral_code_list_url: str, api_client: APIClient, user: User):
    data = {
        'name': 'code',
        'is_active': True
    }
    response = api_client.post(referral_code_list_url, data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_referral_code_delete_authorized(referral_code_url: str, api_client: APIClient, user: User):
    api_client.force_authenticate(user)
    response = api_client.delete(referral_code_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_referral_code_delete_unauthorized(referral_code_url: str, api_client: APIClient, user: User):
    response = api_client.delete(referral_code_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_referral_code_put_authorized(api_client: APIClient, user: User, referral_code: ReferralCode,
                                      referral_code_url):
    api_client.force_authenticate(user)
    data = {
        'name': 'abcd',
        'is_active': False
    }
    response = api_client.put(referral_code_url, data=data)
    assert response.status_code == status.HTTP_200_OK
    referral_code.refresh_from_db(fields=('name', 'is_active'))
    assert response.data['name'] == referral_code.name
    assert response.data['is_active'] == referral_code.is_active


@pytest.mark.django_db
def test_referral_code_put_unauthorized(api_client: APIClient, user: User, referral_code_url: str,
                                        referral_code: ReferralCode):
    data = {
        'name': 'abcd',
        'is_active': False
    }
    response = api_client.put(referral_code_url, data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# Тесты для Balance.
@pytest.mark.django_db
def test_balance_get_authorized(user: User, api_client: APIClient, balance_url: str):
    api_client.force_authenticate(user)
    response = api_client.get(balance_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['uuid'] == str(user.balance.uuid)
    assert response.data['value'] == user.balance.value
    assert response.data['user'] == user.username


# Тесты на Profile.
@pytest.mark.django_db
def test_profile_get_list_authorized(user: User, api_client: APIClient, profile_list_url: str, profile: Profile):
    api_client.force_authenticate(user)
    response = api_client.get(profile_list_url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == Profile.objects.count()


@pytest.mark.django_db
def test_profile_get_list_unauthorized(user: User, api_client: APIClient, profile_list_url: str, profile: Profile):
    response = api_client.get(profile_list_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_profile_get_detail_authorized(user: User, api_client: APIClient, profile_url: str, profile: Profile):
    api_client.force_authenticate(user)
    response = api_client.get(profile_url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 10
    assert response.data['uuid'] == str(profile.uuid)
    assert response.data['age'] == profile.age
    assert response.data['telegram_profile'] == profile.telegram_profile
    assert response.data['telegram_channel'] == profile.telegram_channel
    assert response.data['telegram_subscribers'] == profile.telegram_subscribers
    assert response.data['youtube_profile'] == profile.youtube_profile
    assert response.data['youtube_channel'] == profile.youtube_channel
    assert response.data['youtube_subscribers'] == profile.youtube_subscribers
    assert response.data['status'] == profile.status
    assert response.data['user'] == user.username
    assert 'id' not in response.data


@pytest.mark.django_db
def test_profile_get_detail_unauthorized(user: User, api_client: APIClient, profile_url: str, profile: Profile):
    response = api_client.get(profile_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_profile_post_authorized(user: User, api_client: APIClient, profile_list_url: str):
    api_client.force_authenticate(user)
    data = {
        'age': 25,
        'telegram_profile': '@testuser',
        'telegram_channel': '@testchannel',
        'telegram_subscribers': 55,
        'youtube_profile': 'testuser',
        'youtube_channel': 'testchannel',
        'youtube_subscribers': 11,
        'status': False
    }
    response = api_client.post(profile_list_url, data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.data) == 10
    assert response.data['uuid'] == str(user.profile.uuid)
    assert response.data['age'] == user.profile.age
    assert response.data['telegram_profile'] == user.profile.telegram_profile
    assert response.data['telegram_channel'] == user.profile.telegram_channel
    assert response.data['telegram_subscribers'] == user.profile.telegram_subscribers
    assert response.data['youtube_profile'] == user.profile.youtube_profile
    assert response.data['youtube_channel'] == user.profile.youtube_channel
    assert response.data['youtube_subscribers'] == user.profile.youtube_subscribers
    assert response.data['status'] == user.profile.status
    assert response.data['user'] == user.username
    assert 'id' not in response.data


@pytest.mark.django_db
def test_profile_post_unauthorized(user: User, api_client: APIClient, profile_list_url: str):
    data = {
        'age': 25,
        'telegram_profile': '@testuser',
        'telegram_channel': '@testchannel',
        'telegram_subscribers': 55,
        'youtube_profile': 'testuser',
        'youtube_channel': 'testchannel',
        'youtube_subscribers': 11,
        'status': False
    }
    response = api_client.post(profile_list_url, data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_profile_put_authorized(user: User, api_client: APIClient, profile_url: str, profile: Profile):
    api_client.force_authenticate(user)
    data = {
        'age': 100,
        'telegram_profile': '@testuserrr',
        'telegram_channel': '@testchannelll',
        'telegram_subscribers': 55000,
        'youtube_profile': 'testuserrr',
        'youtube_channel': 'testchannelll',
        'youtube_subscribers': 111111,
        'status': False
    }
    response = api_client.put(profile_url, data=data)
    profile.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 10
    assert response.data['uuid'] == str(profile.uuid)
    assert response.data['age'] == profile.age
    assert response.data['telegram_profile'] == profile.telegram_profile
    assert response.data['telegram_channel'] == profile.telegram_channel
    assert response.data['telegram_subscribers'] == profile.telegram_subscribers
    assert response.data['youtube_profile'] == profile.youtube_profile
    assert response.data['youtube_channel'] == profile.youtube_channel
    assert response.data['youtube_subscribers'] == profile.youtube_subscribers
    assert response.data['status'] == profile.status
    assert response.data['user'] == user.username
    assert 'id' not in response.data


@pytest.mark.django_db
def test_profile_put_authorized(user: User, api_client: APIClient, profile_url: str, profile: Profile):
    data = {
        'age': 100,
        'telegram_profile': '@testuserrr',
        'telegram_channel': '@testchannelll',
        'telegram_subscribers': 55000,
        'youtube_profile': 'testuserrr',
        'youtube_channel': 'testchannelll',
        'youtube_subscribers': 111111,
        'status': False
    }
    response = api_client.put(profile_url, data=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_profile_delete_authorized(user: User, api_client: APIClient, profile_url: str, profile: Profile):
    api_client.force_authenticate(user)
    response = api_client.delete(profile_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None


@pytest.mark.django_db
def test_profile_delete_authorized(user: User, api_client: APIClient, profile_url: str, profile: Profile):
    response = api_client.delete(profile_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_referral_register(api_client: APIClient, referral_register_url: str):
    data = {
        "username": "referral",
        "password": "Roma1908",
        "first_name": "referral",
        "last_name": "refferral",
        "email": "refferral@mail.ru",
        "is_blogger": False
    }
    response = api_client.post(referral_register_url, data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.data) == 8
    referral = User.objects.get(uuid=response.data['uuid'])
    assert str(referral.uuid) == response.data['uuid']
    assert referral.username == response.data['username']
    assert referral.referrer.username == response.data['referrer']
    assert referral.first_name == response.data['first_name']
    assert referral.last_name == response.data['last_name']
    assert referral.email == response.data['email']
    assert referral.status == response.data['status']
    assert referral.is_blogger == response.data['is_blogger']
    assert referral.balance.value == 0
