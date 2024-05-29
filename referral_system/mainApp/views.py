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
import asyncio
from asgiref.sync import sync_to_async
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from adrf.views import APIView as AsyncAPIView
from django.contrib.auth import get_user_model


# Асинхронное представление с использованием библиотеки adrf.
# Асинхронно получаем список рефералов
class AsyncReferralList(AsyncAPIView):
    async def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        referrals = User.objects.filter(referrer_id=pk)
        serializer = AsyncUserSerializer(referrals, many=True)
        data = await sync_to_async(lambda: serializer.data)()
        return Response({'referrals': data})


# Асинхронно регистрируем нового пользователя.
class AsyncUserRegister(AsyncAPIView):
    permission_classes = (AllowAny,)

    async def post(self, request):
        user = await User.objects.acreate(
            username=request.data['username'],
            password=request.data['password']
        )
        serializer = AsyncUserSerializer(user)
        data = await sync_to_async(lambda: serializer.data)()
        return Response({'user': data})


# Асинхронно создаем реферальный код.
class AsyncReferralCodeListCreateView(AsyncAPIView):
    permission_classes = (IsAuthenticated,)

    async def post(self, request):
        referral_code = await ReferralCode.objects.acreate(
            name=request.data['name'],
            user=request.user,
            is_active=False
        )
        serializer = AsyncReferralCodeSerializer(referral_code)
        data = await sync_to_async(lambda: serializer.data)()
        return Response({'referral_code': data})


#Асинхронно удаляем реф код.
class AsyncReferralCodeDetailUpdateDeleteView(AsyncAPIView):
    permission_classes = (IsAuthenticated, )

    async def delete(self, request, **kwargs):
        pk = self.kwargs['pk']
        await ReferralCode.objects.filter(pk=pk).adelete()
        return Response({'response': 'Referral code deleted.'})

#Асинхронно регисрируем реферала по коду.
class AsyncReferralRegister(AsyncAPIView):
    async def post(self, request, **kwargs):
        pk = self.kwargs['pk']
        referral_code = await ReferralCode.objects.aget(pk=pk)
        if not referral_code.is_active or not referral_code.life_time():
            return Response({'response': 'This referral code is not active.'})
        referrer = referral_code.user
        referral = await User.objects.acreate(
            username=request.data['username'],
            password=request.data['password'],
            referrer=referrer
        )
        serializer = AsyncUserSerializer(referral)
        data = await sync_to_async(serializer.data)()
        return Response({'referral': data})


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
        if not referral_code.is_active:
            return Response({'response': 'This referral code is not active.'})
        else:
            if not referral_code.life_time():
                return Response({'response': 'This referral code is not active.'})
            else:
                referrer = referral_code.user
                referral = User.objects.create(
                    username=request.data['username'],
                    password=request.data['password'],
                    referrer=referrer
                )
                return Response({'referral': UserSerializer(referral).data})


# Асинхронное предсатвление, возвращает корутину.
# class ReferralList(APIView):
#     # permission_classes = (IsAuthenticated,)
#
#     async def get(self, request, **kwargs):
#         pk = self.kwargs['pk']
#         referrals = await User.objects.filter(referrer_id=pk)
#         return Response({'referrals': UserSerializer(referrals, many=True).data})


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
async def referral_list(request, pk):
    referrals = User.objects.filter(referrer_id=pk)
    serializer = UserSerializer(referrals, many=True)
    data = await sync_to_async(lambda: serializer.data)()
    return Response({'referrals': data})


# Регистрация нового пользователя.
class UserRegister(APIView):
    permission_classes = (AllowAny,)

    async def post(self, request):
        user = await User.objects.acreate(
            username=request.data['username'],
            password=request.data['password']
        )
        serializer = UserSerializer(user)
        data = await sync_to_async(lambda: serializer.data)()
        return Response({'user': data})
