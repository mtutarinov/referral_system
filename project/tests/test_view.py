import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import User, ReferralCode
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
    assert datetime.strptime(response.data['create_date'], "%Y-%m-%dT%H:%M:%S.%fZ") == referral_code.create_date.replace(tzinfo=None)
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
def test_referral_code_put_authorized(api_client: APIClient, user: User):
    code = ReferralCodeFactory.create(user=user)
    api_client.force_authenticate(user)
    data = {
        'name': 'abcd',
        'is_active': False
    }
    response = api_client.put(reverse('core:referralcode-detail', args=(str(code.uuid),)), data=data)
    assert response.status_code == status.HTTP_200_OK
    code.refresh_from_db(fields=('name', 'is_active'))
    assert response.data['name'] == code.name
    assert response.data['is_active'] == code.is_active
