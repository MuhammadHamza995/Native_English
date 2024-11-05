from django.urls import path, include
from .views import AdminUserListCreateView, AdminUserRetrieveUpdateView

urlpatterns = [
    path('users/', AdminUserListCreateView.as_view(), name='user-create-list'),
    path('users/<int:id>/', AdminUserRetrieveUpdateView.as_view(), name='user-detail'),

]