import datetime

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from .serializers import UserListSerializer, UserDetailSerializer, ReferralCodeListSerializer, ProfileListSerializer, \
    ProfileDetailSerializer, ReferralCodeDetailSerializer, BalanceListSerializer, BalanceDetailSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import ReferralCode, User, Profile, Balance
from django.http import JsonResponse
from rest_framework import viewsets
from django.db import transaction
from .tasks import add_money_to_referrer_referral_balance
from .paginations import CorePagination


class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related('referrer').only('uuid', 'referrer__username', 'username', 'status',
                                                                  'created_at')
    lookup_field = 'uuid'
    pagination_class = CorePagination

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        return UserDetailSerializer


class ProfileViewSets(viewsets.ModelViewSet):
    queryset = Profile.objects.all().select_related('user', 'balance').only(
        'uuid', 'status', 'user__username', 'balance__value', 'created_at')
    lookup_field = 'uuid'
    pagination_class = CorePagination

    # permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'list':
            return ProfileListSerializer
        return ProfileDetailSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReferralCodeViewSets(viewsets.ModelViewSet):
    queryset = ReferralCode.objects.all()
    # permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.action == 'list':
            return ReferralCodeListSerializer
        return ReferralCodeDetailSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BalanceViewSets(viewsets.ModelViewSet):
    queryset = Balance.objects.all().select_related('user').only('uuid', 'user__username', 'created_at')
    # permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'
    pagination_class = CorePagination

    def get_serializer_class(self):
        if self.action == 'list':
            return BalanceListSerializer
        return BalanceDetailSerializer


class ReferralRegister(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (AllowAny,)

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(referrer=User.objects.get(referral_codes__uuid=self.kwargs['uuid']))
        add_money_to_referrer_referral_balance.delay(id=serializer.instance.id)


class ReferralList(ListAPIView):
    serializer_class = UserListSerializer

    def get_queryset(self):
        return User.objects.select_related('referrer').only('uuid', 'referrer__username', 'username', 'status',
                                                            'created_at').filter(referrer=self.kwargs['pk'])
