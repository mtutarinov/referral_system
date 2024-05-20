from django.urls import path, include, re_path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = 'mainApp'
urlpatterns = [
    path('api/user_register/', UserRegister.as_view(), name='user_register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/referral_code_create/', ReferralCodeCreate.as_view(), name='referral_code_create'),
    path('api/referral_code_delete/<int:pk>/', ReferralCodeDelete.as_view(), name='referral_code_delete'),
    path('api/referral_register/<int:pk>/', ReferralRegister.as_view(), name='referral_register'),
    path('api/referral_list/<int:pk>/', ReferralList.as_view(), name='referral_list'),
    # re_path(r'^auth/', include('drf_social_oauth2.urls', namespace='drf')),
]
