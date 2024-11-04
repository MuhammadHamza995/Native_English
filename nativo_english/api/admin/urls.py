from django.urls import path, include
from .views import AdminUserCreateView

urlpatterns = [
    path('user', AdminUserCreateView.as_view(), name='Create-USER-By-ADMIN'),
]