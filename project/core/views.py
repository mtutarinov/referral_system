import datetime

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from .serializers import UserReadSerializer, UserCreateSerializer, ReferralCodeReadSerializer, ProfileReadSerializer, \
    ProfileCreateSerializer, ReferralCodeCreateSerializer, BalanceSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import ReferralCode, User, Profile, Balance
from django.http import JsonResponse
from rest_framework import viewsets
from django.db import transaction


class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all()

    # lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return UserCreateSerializer
        return UserReadSerializer


class ProfileViewSets(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.method in ("POST", "PUT"):
            return ProfileCreateSerializer
        return ProfileReadSerializer


class ReferralCodeViewSets(viewsets.ModelViewSet):
    queryset = ReferralCode.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.method in ("POST", "PUT"):
            return ReferralCodeCreateSerializer
        return ReferralCodeReadSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BalanceRetrieveAPIView(RetrieveAPIView):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'


class ReferralRegister(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(referrer=User.objects.get(referral_codes__uuid=self.kwargs['uuid']))
