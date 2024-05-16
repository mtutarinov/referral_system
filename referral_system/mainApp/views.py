from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import *
from django.forms.models import model_to_dict
from .models import ReferralCode, User
from rest_framework.renderers import JSONRenderer

# Регистрация нового пользователя.
class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


# Создание юзером реферального кода.
class ReferralCodeCreate(APIView):
    permission_classes = (IsAuthenticated,)

    # Вся работа с моделями происходит в представлении. Данные возвращаются полностью.
    # def post(self, request):
    #     referral_code = ReferralCode.objects.create(
    #         name=request.data['name'],
    #         user=request.user,
    #         is_active=True
    #     )
    #     return Response({'referral_code': ReferralCodeSerializer(referral_code).data})

    # Работа с моделями происходит на стороне сериализатора. В базе данных все сохраняется. В ответе не указан user.
    # def post(self, request):
    #     serializer = ReferralCodeSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(user=request.user)
    #     return Response({'referral_code': serializer.data})

    # #Метод post для сериализатора с CurrentUserDefault.
    # def post(self, request):
    #     serializer = ReferralCodeSerializer(data=request.data, context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response({'referral_code': serializer.data})

    # Mетод post для сериализатора с методом validate.
    def post(self, request):
        serializer = ReferralCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'referral_code': serializer.data})

    # def delete(self, request):
    #     referral_code = ReferralCode.objects.get(pk=request.data['pk'])
    #     referral_code.delete()
    #     return Response({'Код был успешно удален'})


class ReferralCodeDelete(generics.DestroyAPIView):
    queryset = ReferralCode.objects.all()
    serializer_class = ReferralCodeSerializer
    permission_classes = (IsAuthenticated,)


class ReferralRegister(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        pk = self.kwargs['pk']
        referral_code = ReferralCode.objects.get(pk=pk)
        referrer = referral_code.user
        referral = User.objects.create(
            username=request.data['username'],
            password=request.data['password'],
            referrer=referrer
        )
        return Response({'referral': model_to_dict(referral)})


class ReferralList(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        referrer = User.objects.get(pk=pk)
        referrals = referrer.referrals.all()
        return Response({'referrals': UserSerializer(referrals, many=True).data})