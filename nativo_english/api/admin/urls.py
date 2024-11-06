from django.urls import path, include
from .views import AdminUserListCreateView, AdminUserRetrieveUpdateView, AdminUserRoleUpdateView

urlpatterns = [
    path('users/', AdminUserListCreateView.as_view(), name='user-create-list'),
    path('users/<int:id>/', AdminUserRetrieveUpdateView.as_view(), name='user-detail'),

    path('users/<int:id>/role', AdminUserRoleUpdateView.as_view(), name='user-role-update'),

]