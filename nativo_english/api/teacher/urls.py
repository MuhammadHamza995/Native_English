from django.urls import path, include
from .views import (
    TeacherCourseListCreateView, TeacherCourseRetrieveUpdateView, 
    TeacherCourseSectionListCreateView, TeacherCourseSectionRetrieveUpdateView,
    TeacherCourseLessonListCreateView, TeacherCourseLessonRetrieveUpdateView)


urlpatterns = [
    path('course/', TeacherCourseListCreateView.as_view(), name='teacher-course-create-list'),
    path('course/<int:id>/', TeacherCourseRetrieveUpdateView.as_view(), name='teacher-course-detail'),

    path('course/<int:course_id>/section/', TeacherCourseSectionListCreateView.as_view(), name='teacher-course-section-create-list'),
    path('course/<int:course_id>/section/<int:course_section_id>/', TeacherCourseSectionRetrieveUpdateView.as_view(), name='teacher-course-section-detail'),

    path('course/section/<int:course_section_id>/lesson', TeacherCourseLessonListCreateView.as_view(), name='teacher-course-lesson-create-list'),
    path('course/section/<int:course_section_id>/lesson/<int:course_lesson_id>/', TeacherCourseLessonRetrieveUpdateView.as_view(), name='teacher-course-lesson-detail'),
]