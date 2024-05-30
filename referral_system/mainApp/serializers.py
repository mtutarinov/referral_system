from rest_framework import serializers
from .models import *
from adrf.serializers import ModelSerializer as AsyncModelSerializer


# Асинхронный сериализатор для User
class AsyncUserSerializer(AsyncModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# Асинхронный сериализатор для ReferralCode
class AsyncReferralCodeSerializer(AsyncModelSerializer):
    class Meta:
        model = ReferralCode
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# Сериализатор с измененным методом validate
class ReferralCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCode
        fields = ('name', 'is_active', 'user')
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        return attrs

    def create(self, validated_data):
        return ReferralCode.objects.create(**validated_data)
