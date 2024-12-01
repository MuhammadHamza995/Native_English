from django.db import models

class CourseLessonContent(models.Model):
    title = models.CharField(max_length=255)  # Adjust field type and max length based on your DB schema
    content = models.TextField()  # Assuming it's a long text field
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Change the table name to avoid conflicts with other models
        db_table = 'admin_course_lessoncontent'  # New table name for this model

    def __str__(self):
        return self.title

