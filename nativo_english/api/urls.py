from django.urls import path, include
from .shared.auth.views import LoginView, TwoFactorView, VerifyOtpView

# Will be adding all api based urlpatterns here
urlpatterns = [
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('2fa/', TwoFactorView.as_view(), name='two_factor'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify_otp'),

    # Admin API URLs goes here
    path('admin/', include('nativo_english.api.admin.urls')),
]