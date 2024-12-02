from rest_framework import serializers
from .models import Course, CourseSection, CourseLesson

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'is_paid', 'price', 'mode', 'avg_rating', 'is_active', 'owner']
        
class CourseSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSection
        fields = [
            'id', 'section_title', 'section_description', 'fk_course_id']


class CourseLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = [
            'id', 'lesson_title', 'lesson_description', 'lesson_position', 'is_active', 'fk_section_id']