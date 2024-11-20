from django.urls import path, include
from .views import AdminUserListCreateView, AdminUserRetrieveUpdateView, AdminUserRoleUpdateView, AdminUserActivateSuspendUpdateView, AdminCourseListCreateView, AdminCourseRetrieveUpdateView
from .views import CourseImageUploadView
urlpatterns = [
    path('users/', AdminUserListCreateView.as_view(), name='user-create-list'),
    path('users/<int:id>/', AdminUserRetrieveUpdateView.as_view(), name='user-detail'),

    path('users/<int:id>/role', AdminUserRoleUpdateView.as_view(), name='user-role-update'),
    path('users/<int:id>/activate/', AdminUserActivateSuspendUpdateView.as_view(), {'action' : 'activate'}, name='activate-user'),
    path('users/<int:id>/suspend/', AdminUserActivateSuspendUpdateView.as_view(), {'action' : 'suspend'} ,name='suspend-user'),

    path('course/', AdminCourseListCreateView.as_view(), name='course-create-list'),
    path('course/<int:id>/', AdminCourseRetrieveUpdateView.as_view(), name='course-detail'),

    path('upload-course-image/<int:course_id>/', CourseImageUploadView.as_view(), name='upload-course-image'),
]
