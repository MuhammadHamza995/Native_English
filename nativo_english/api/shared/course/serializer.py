from rest_framework import serializers
from .models import Course, CourseSection, CourseLesson, LessonContent

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
        

class LessonContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonContent
        fields = [
            'id', 
            'fk_course_lesson', 
            'content_type', 
            'content_text', 
            'content_audio_url', 
            'content_image_url', 
            'content_video_url',  # Ensure this field is included for video URL
            'created_at', 
            'updated_at'
        ]

    def validate(self, data):
        """
        Ensure that the correct field is provided based on the content_type.
        """
        content_type = data.get('content_type')

        # Validate the content based on type
        if content_type == 'text' and not data.get('content_text'):
            raise serializers.ValidationError("Text content must include 'content_text'.")
        if content_type == 'video' and not data.get('content_video_url'):
            raise serializers.ValidationError("Video content must include 'content_video_url'.")
        if content_type == 'audio' and not data.get('content_audio_url'):
            raise serializers.ValidationError("Audio content must include 'content_audio_url'.")
        if content_type == 'image' and not data.get('content_image_url'):
            raise serializers.ValidationError("Image content must include 'content_image_url'.")

        return data


    def create(self, validated_data):
        """
        Custom logic for storing the URL or path of files and creating the lesson content instance.
        """
        # Example: You might handle additional file upload or processing logic here
        instance = LessonContent.objects.create(**validated_data)
        return instance

    
