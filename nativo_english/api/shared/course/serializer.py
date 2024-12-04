from rest_framework import serializers
from .models import Course, CourseSection, CourseLesson, LessonContent

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'is_paid', 'price', 'mode', 'level', 'avg_rating', 'is_active', 'owner']
        
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
        

class LessonContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonContent
        fields = '__all__'

    def validate(self, data):
        content_type = data.get('content_type')

        if content_type == 'text' and not data.get('content_text'):
            raise serializers.ValidationError("Text content must include 'content_text'.")
        if content_type == 'video' and not data.get('content_video_url'):
            raise serializers.ValidationError("Video content must include 'content_video_url'.")
        if content_type == 'audio' and not data.get('content_audio_url'):
            raise serializers.ValidationError("Audio content must include 'content_audio_url'.")
        if content_type == 'image' and not data.get('content_image_url'):
            raise serializers.ValidationError("Image content must include 'content_image_url'.")
        
        return data