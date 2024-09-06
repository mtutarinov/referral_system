import datetime

from rest_framework import serializers
from .models import User, ReferralCode, Profile, Balance


class UserListSerializer(serializers.ModelSerializer):
    referrer = serializers.SlugRelatedField(slug_field='username', queryset=User.objects)

    class Meta:
        model = User
        fields = ('uuid', 'referrer', 'username', 'status', 'created_at')


class UserDetailSerializer(serializers.ModelSerializer):
    referrer = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = User
        fields = ('uuid', 'referrer', 'username', 'first_name', 'last_name', 'email', 'status', 'is_blogger', 'created_at')


class ProfileListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    balance = serializers.SlugRelatedField(slug_field='value', read_only=True)

    class Meta:
        model = Profile
        fields = (
            'uuid', 'status', 'user', 'balance', 'created_at')


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Profile
        fields = (
            'uuid', 'age', 'telegram_profile', 'telegram_channel', 'telegram_subscribers', 'youtube_profile',
            'youtube_channel',
            'youtube_subscribers', 'status', 'user')


class ReferralCodeListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = ReferralCode
        fields = ('uuid', 'user', 'create_date')


class ReferralCodeDetailSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = ReferralCode
        fields = ('uuid', 'name', 'user', 'create_date', 'is_active')


class BalanceListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Balance
        fields = ('uuid', 'user', 'created_at')

class BalanceDetailSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Balance
        fields = ('uuid', 'user', 'created_at', 'value')
