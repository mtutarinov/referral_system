from django.urls import path, include, re_path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = 'mainApp'
urlpatterns = [
    path('api/user_register/', AsyncUserRegister.as_view(), name='user_register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/referral_code/', AsyncReferralCodeListCreateView.as_view(), name='referral_code_create'),
    path('api/referral_code/<int:pk>/', AsyncReferralCodeDetailUpdateDeleteView.as_view(), name='referral_code_delete'),
    path('api/referral_register/<int:pk>/', AsyncReferralRegister.as_view(), name='referral_register'),
    path('api/referral_list/<int:pk>/', AsyncReferralList.as_view(), name='referral_list'),
]
