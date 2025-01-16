from django.urls import path, include
from nativo_english.api.shared.auth.views import LoginView, TwoFactorView, VerifyOtpView, ForgotPasswordView, UpdatePasswordView, ResendOtpView, LogoutView

# Will be adding all api based urlpatterns here
urlpatterns = [
    
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout_user'),
    path('2fa/', TwoFactorView.as_view(), name='two_factor'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify_otp'),
    path('resend-otp/', ResendOtpView.as_view(), name='resend-otp'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('update-password/', UpdatePasswordView.as_view(), name='update-password'),
    

    # Admin API URLs goes here
    path('admin/', include('nativo_english.api.admin.urls')),

    # Teacher API URLs goes here
    path('teacher/', include('nativo_english.api.teacher.urls'))

]





