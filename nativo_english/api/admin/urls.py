from django.urls import path
from .views import (
    AdminUserListCreateView,
    AdminUserRetrieveUpdateView,
    AdminUserRoleUpdateView,
    AdminUserActivateSuspendUpdateView,
    AdminCourseListCreateView,
    AdminCourseRetrieveUpdateView,
    AdminCourseSectionListCreateView,
    AdminCourseSectionRetrieveUpdateView,
    AdminCourseLessonListCreateView,
    AdminCourseLessonRetrieveUpdateView,
    AdminCourseLessonContentRetrieveUpdateView
)

urlpatterns = [
    # Users
    path('users/', AdminUserListCreateView.as_view(), name='user-create-list'),
    path('users/<int:id>/', AdminUserRetrieveUpdateView.as_view(), name='user-detail'),
    path('users/<int:id>/role', AdminUserRoleUpdateView.as_view(), name='user-role-update'),
    path('users/<int:id>/<str:action>/', AdminUserActivateSuspendUpdateView.as_view(), name='activate-suspend-user'),

    # Courses
    path('course/', AdminCourseListCreateView.as_view(), name='course-create-list'),
    path('course/<int:id>/', AdminCourseRetrieveUpdateView.as_view(), name='course-detail'),

    # Course Sections
    path('course/section/', AdminCourseSectionListCreateView.as_view(), name='course-section-create-list'),
    path('course/section/<int:course_section_id>/', AdminCourseSectionRetrieveUpdateView.as_view(), name='course-section-detail'),

    # Course Lessons
    path('course/section/lesson', AdminCourseLessonListCreateView.as_view(), name='course-lesson-create-list'),
    path('course/section/lesson/<int:course_lesson_id>/', AdminCourseLessonRetrieveUpdateView.as_view(), name='course-lesson-detail'),

    # Course Lesson Content
    path('course_lesson_content/<int:course_lesson_content_id>/', AdminCourseLessonContentRetrieveUpdateView.as_view(), name='course_lesson_content_detail'),
]
