from rest_framework import serializers
from .models import Course, CourseSection, CourseLesson, LessonContent
from nativo_english.api.shared.upload_engine import handle_file_upload

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
            'fk_course_lesson_id', 
            'content_type', 
            'content_text', 
            'content_audio',   # Updated field name
            'content_image',   # Updated field name
            'content_video',   # Updated field name
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
        if content_type == 'video' and not data.get('content_video'):
            raise serializers.ValidationError("Video content must include 'content_video'.")
        if content_type == 'audio' and not data.get('content_audio'):
            raise serializers.ValidationError("Audio content must include 'content_audio'.")
        if content_type == 'image' and not data.get('content_image'):
            raise serializers.ValidationError("Image content must include 'content_image'.")

        return data

    def create(self, validated_data):
        """
        Custom logic for storing the URL or path of files and creating the lesson content instance.
        """
        # Handle file uploads in case of file fields (video, audio, image)
        content_video_url = validated_data.get('content_video_url', None)
        content_audio_url = validated_data.get('content_audio_url', None)
        content_image_url = validated_data.get('content_image_url', None)

        if content_video_url:
            validated_data['content_video_url'] = handle_file_upload(content_video_url, allowed_extensions=['.mp4'])
        
        if content_audio_url:
            validated_data['content_audio_url'] = handle_file_upload(content_audio_url, allowed_extensions=['.mp3'])
        
        if content_image_url:
            validated_data['content_image_url'] = handle_file_upload(content_image_url, allowed_extensions=['.jpg', '.png', '.jpeg'])
        
        # Create the LessonContent instance
        instance = LessonContent.objects.create(**validated_data)
        return instance

    
