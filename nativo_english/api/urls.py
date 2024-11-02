from django.urls import path, include
from .shared.auth.views import LoginView

# Will be adding all api based urlpatterns here
urlpatterns = [
    path('login/', LoginView.as_view(), name='token_obtain_pair')
]