import datetime

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .serializers import UserReadSerializer, UserCreateSerializer, ReferralCodeReadSerializer, ProfileReadSerializer, \
    ProfileCreateSerializer, ReferralCodeCreateSerializer, BalanceSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import ReferralCode, User, Profile, Balance
from django.http import JsonResponse
from rest_framework import viewsets


class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return UserCreateSerializer
        return UserReadSerializer


class ProfileViewSets(viewsets.ModelViewSet):
    queryset = Profile.objects.all()

    def get_serializer_class(self):
        if self.request.method in ("POST", "PUT"):
            return ProfileCreateSerializer
        return ProfileReadSerializer


class ReferralCodeViewSets(viewsets.ModelViewSet):
    queryset = ReferralCode.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method in ("POST", "PUT"):
            return ReferralCodeCreateSerializer
        return ReferralCodeReadSerializer


class BalanceRetrieveAPIView(RetrieveAPIView):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    permission_classes = (IsAuthenticated,)

# Прикрутить свагер
