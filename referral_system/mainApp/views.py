from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import *
from .models import ReferralCode, User
from django.http import JsonResponse
from adrf.views import APIView as AsyncAPIView


# Асинхронно получаем список рефералов
class AsyncReferralList(AsyncAPIView):
    async def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        referrals = User.objects.filter(referrer_id=pk)
        serializer = AsyncUserSerializer(referrals, many=True)
        data = await serializer.adata
        return Response({'referrals': data})


# Асинхронно регистрируем нового пользователя.
class AsyncUserRegister(AsyncAPIView):
    permission_classes = (AllowAny,)

    # @transaction.atomic()
    async def post(self, request):
        user = User.objects.create(
            username=request.data['username'],
            password=request.data['password']
        )
        print(type(user))
        serializer = AsyncUserSerializer(user)
        data = await serializer.adata
        return JsonResponse({'user': data})


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
        data = await serializer.adata
        return Response({'referral_code': data})


# Асинхронно удаляем реф код.
class AsyncReferralCodeDetailUpdateDeleteView(AsyncAPIView):
    permission_classes = (IsAuthenticated,)

    async def delete(self, request, pk):
        await ReferralCode.objects.filter(pk=pk).adelete()
        return Response({'response': 'Referral code deleted.'})


# Асинхронно регисрируем реферала по коду.
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
        data = await serializer.adata
        return Response({'referral': data})


# Создание юзером реферального кода.
class ReferralCodeCreate(APIView):
    permission_classes = (IsAuthenticated,)

    # Mетод post для сериализатора с методом validate.
    def post(self, request):
        serializer = ReferralCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'referral_code': serializer.data})
