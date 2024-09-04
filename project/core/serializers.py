import datetime

from rest_framework import serializers
from .models import User, ReferralCode, Profile, Balance


class UserListSerializer(serializers.ModelSerializer):
    referrer = serializers.SlugRelatedField(slug_field='username', queryset=User.objects)

    class Meta:
        model = User
        fields = ('uuid', 'referrer', 'username', 'status')


class UserDetailSerializer(serializers.ModelSerializer):
    referrer = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = User
        fields = ('uuid', 'referrer', 'username', 'first_name', 'last_name', 'email', 'status', 'is_blogger',)


class ProfileReadSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Profile
        fields = (
            'uuid', 'age', 'telegram_profile', 'telegram_channel', 'telegram_subscribers', 'youtube_profile',
            'youtube_channel',
            'youtube_subscribers', 'status', 'user')


class ProfileCreateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Profile
        fields = (
            'uuid', 'age', 'telegram_profile', 'telegram_channel', 'telegram_subscribers', 'youtube_profile',
            'youtube_channel',
            'youtube_subscribers', 'status', 'user')


class ReferralCodeReadSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = ReferralCode
        fields = ('uuid', 'name', 'user', 'create_date', 'is_active')


class ReferralCodeCreateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = ReferralCode
        fields = ('uuid', 'name', 'user', 'create_date', 'is_active')


class BalanceSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField()
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Balance
        fields = ('uuid', 'value', 'user')
