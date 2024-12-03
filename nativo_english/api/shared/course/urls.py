# shared/course/urls.py



from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.get_all_courses, name='get_all_courses'),
    path('courses/<int:course_id>/', views.get_course_by_id, name='get_course_by_id'),
    path('courses/create/', views.create_course, name='create_course'),
    path('courses/<int:course_id>/update/', views.update_course, name='update_course'),
    path('course_sections/', views.get_all_course_sections, name='get_all_course_sections'),
    path('course_sections/<int:course_section_id>/', views.get_course_section_by_id, name='get_course_section_by_id'),
    path('course_sections/create/', views.create_course_section, name='create_course_section'),
    path('course_lessons/', views.get_all_course_lessons, name='get_all_course_lessons'),
    path('course_lessons/<int:course_lesson_id>/', views.get_course_lesson_by_id, name='get_course_lesson_by_id'),
    path('course_lessons/create/', views.create_course_lesson, name='create_course_lesson'),
    # Update the endpoint to create lesson content, passing lesson_id in the body, not in the URL
    path('lesson_content/create/', views.create_lesson_content, name='create_lesson_content'),
]

