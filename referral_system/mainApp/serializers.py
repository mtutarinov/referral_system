from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# Сериализато для метода post, где serializer.save(user=request.user)
# class ReferralCodeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ReferralCode
#         exclude = ['user']
#
#     def create(self, validated_data):
#         return ReferralCode.objects.create(**validated_data)


# Сериализатор с CurrentUserDefault.
# class ReferralCodeSerializer(serializers.ModelSerializer):
#     user = serializers.CharField(
#         default=serializers.CurrentUserDefault()
#     )
#
#     class Meta:
#         model = ReferralCode
#         fields = ('name', 'is_active', 'user')
#
#     def create(self, validated_data):
#         return ReferralCode.objects.create(**validated_data)


#Сериализатор с измененным методом validate
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


