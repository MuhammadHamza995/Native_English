from django.urls import path, include
from .views import (
    AdminUserListCreateView, AdminUserRetrieveUpdateView, AdminUserRoleUpdateView, AdminUserActivateSuspendUpdateView, 
    AdminCourseListCreateView, AdminCourseRetrieveUpdateView, 
    AdminCourseSectionListCreateView, AdminCourseSectionRetrieveUpdateView, 
    AdminCourseLessonListCreateView, AdminCourseLessonRetrieveUpdateView,
    AdminCourseLessonContentListCreateView)

urlpatterns = [
    path('users/', AdminUserListCreateView.as_view(), name='user-create-list'),
    path('users/<int:id>/', AdminUserRetrieveUpdateView.as_view(), name='user-detail'),
    path('users/<int:id>/role', AdminUserRoleUpdateView.as_view(), name='user-role-update'),
    path('users/<int:id>/<str:action>/', AdminUserActivateSuspendUpdateView.as_view(), name='activate-suspend-user'),
    
    path('course/', AdminCourseListCreateView.as_view(), name='course-create-list'),
    path('course/<int:id>/', AdminCourseRetrieveUpdateView.as_view(), name='course-detail'),

    path('course/section/', AdminCourseSectionListCreateView.as_view(), name='course-section-create-list'),
    path('course/section/<int:course_section_id>/', AdminCourseSectionRetrieveUpdateView.as_view(), name='course-section-detail'),

    path('course/section/lesson', AdminCourseLessonListCreateView.as_view(), name='course-lesson-create-list'),
    path('course/section/lesson/<int:course_lesson_id>/', AdminCourseLessonRetrieveUpdateView.as_view(), name='course-lesson-detail'),

    # Keep only one endpoint for handling lesson content
    path('course/section/lesson/<int:lesson_id>/content/', AdminCourseLessonContentListCreateView.as_view(), name='course-section-lesson-content-create-list'),
]


