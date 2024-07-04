import datetime

from rest_framework import serializers
from .models import User, ReferralCode, Profile, Balance


class UserReadSerializer(serializers.ModelSerializer):
    referrer = serializers.SlugRelatedField(slug_field='username', queryset=User.objects)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    status = serializers.BooleanField(read_only=True)
    is_blogger = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('referrer', 'username', 'first_name', 'last_name', 'email', 'status', 'is_blogger',)


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('referrer', 'username', 'first_name', 'last_name', 'email', 'status', 'is_blogger',)


class ProfileReadSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(read_only=True)
    telegram_profile = serializers.CharField(read_only=True)
    telegram_channel = serializers.CharField(read_only=True)
    telegram_subscribers = serializers.IntegerField(read_only=True)
    youtube_profile = serializers.CharField(read_only=True)
    youtube_channel = serializers.CharField(read_only=True)
    youtube_subscribers = serializers.IntegerField(read_only=True)
    status = serializers.BooleanField(read_only=True)
    user = UserReadSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = (
            'age', 'telegram_profile', 'telegram_channel', 'telegram_subscribers', 'youtube_profile', 'youtube_channel',
            'youtube_subscribers', 'status', 'user')


class ProfileCreateSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(write_only=True)
    telegram_profile = serializers.CharField(write_only=True)
    telegram_channel = serializers.CharField(write_only=True)
    telegram_subscribers = serializers.IntegerField(write_only=True)
    youtube_profile = serializers.CharField(write_only=True)
    youtube_channel = serializers.CharField(write_only=True)
    youtube_subscribers = serializers.IntegerField(write_only=True)
    status = serializers.BooleanField(write_only=True)

    class Meta:
        model = Profile
        fields = (
            'age', 'telegram_profile', 'telegram_channel', 'telegram_subscribers', 'youtube_profile', 'youtube_channel',
            'youtube_subscribers', 'status')


class ReferralCodeReadSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    user = UserReadSerializer(read_only=True)
    create_date = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = ReferralCode
        fields = ('name', 'user', 'create_date', 'is_active')


# Сделать вложенный сериализатор для Юзеров и замерить с id или без скорость выполнения


class ReferralCodeCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    user = UserReadSerializer()
    create_date = serializers.DateTimeField()
    is_active = serializers.BooleanField()

    class Meta:
        model = ReferralCode
        fields = ('name', 'user', 'create_date', 'is_active')


class BalanceSerializer(serializers.ModelSerializer):

    money = serializers.IntegerField()
    user = UserReadSerializer()
    class Meta:
        model = Balance
        fields = ('money', 'user')





# Сделать вложенный сериализатор для Юзеров и замерить с id или без скорость выполнения