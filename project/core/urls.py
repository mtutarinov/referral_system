from django.urls import path, include, re_path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework import routers

profile_router = routers.SimpleRouter()
profile_router.register(r'profile', ProfileViewSets)
user_router = routers.SimpleRouter()
user_router.register(r'user', UserViewSets)
referral_code_router = routers.SimpleRouter()
referral_code_router.register(r'referral_code', ReferralCodeViewSets)
balance_router = routers.SimpleRouter()
balance_router.register(r'balance', BalanceViewSets)


app_name = 'core'
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/', include(user_router.urls)),
    path('api/v1/', include(profile_router.urls)),
    path('api/v1/', include(referral_code_router.urls)),
    path('api/v1/', include(balance_router.urls)),
    path('api/v1/referral_register/<str:uuid>/', ReferralRegister.as_view(), name='referral_register'),
    path('api/v1/referral_list/<int:pk>/', ReferralList.as_view(), name='referral_list')
]
