from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class CourseImage(models.Model):
    course = models.ForeignKey(Course, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='course_images/')  
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)  # Added image_url field

    def __str__(self):
        return f"Image for {self.course.name}"


