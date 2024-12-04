from django.urls import path, include
from .views import TeacherCourseListCreateView, TeacherCourseRetrieveUpdateView


urlpatterns = [
    path('course/', TeacherCourseListCreateView.as_view(), name='course-create-list'),
    path('course/<int:id>/', TeacherCourseRetrieveUpdateView.as_view(), name='course-detail'),
]