from django.db import models
from django.conf import settings
from nativo_english.api.shared.user.models import User


# Course Model
class Course(models.Model):
    
    MODE_CHOICES = {
        ('self', 'Self-pace'),
        ('live', 'live'),
    }

    title = models.CharField(max_length=200)
    description = models.TextField()
    is_paid = models.BooleanField(default=False)
    price = models.FloatField(null=True)
    mode = models.CharField(choices=MODE_CHOICES, null=False)
    avg_rating = models.FloatField(max_length=5)    
    is_active = models.BooleanField(default=False)

    # Default Metadata fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_created')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_modified')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Lesson Model of Course
class CourseLesson(models.Model):
    lesson_title = models.CharField(max_length=200)
    lesson_description = models.TextField(null=True)
    lesson_position = models.PositiveIntegerField()
    fk_course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    # Default Metadata fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='lesson_created')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='lesson_modified')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['lesson_position']  # This makes sure the lessons are ordered by the 'lesson_position' field


# Content Model of Lesson of a course
class LessonContent(models.Model):

    CONTENT_TYPE_CHOICES = (
        ('text', 'Text'),
        ('audio', 'Audio'),
        ('video', 'video')
    )

    content_title = models.CharField(max_length=200, null=True)
    lesson_content_position = models.PositiveIntegerField()
    fk_course_lesson_id = models.ForeignKey(CourseLesson, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    language = models.CharField(max_length=7, choices=settings.LANGUAGES)  # Use Django's built-in language list
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES, default='text')
    content_text = models.TextField(blank=True, null=True)  # Text content
    content_video_url = models.URLField(blank=True, null=True)  # Video URL, optional
    content_audio_url = models.URLField(blank=True, null=True)  # Audio URL, optional
    content_image_url = models.URLField(blank=True, null=True)  # Image URL, optional

    # Default Metadata fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='lesson_content_created')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='lesson_content_modified')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['lesson_content_position']  # This makes sure the lessons are ordered by the 'lesson_content_position' field

# # Content Translation
# class ContentTranslation(models.Model):


#     # Default Metadata fields
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# Course Enrollment Model
class CourseEnrollment(models.Model):
    fk_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    fk_course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    # Default Metadata fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_enrollment_created')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_enrollment_modified')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Course Ratings
class CourseRating(models.Model):
    fk_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    fk_course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.FloatField(max_length=5)

    # Default Metadata fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_rating_created')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_rating_modified')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Course Feedback
class CourseFeedback(models.Model):
    fk_course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    fk_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_feedback_id = models.IntegerField(default=0)
    content = models.TextField()

    # Default Metadata fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_feedback_created')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_feedback_modified')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)