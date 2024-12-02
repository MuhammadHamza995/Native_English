from django.db import models

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.title  # Or use any other field you want to represent
    
class CourseSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Link each section to a specific course
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title  # Or any other field you want to represent

class CourseLesson(models.Model):
    course_section = models.ForeignKey(CourseSection, on_delete=models.CASCADE)  # Link lesson to a course section
    title = models.CharField(max_length=100)
    content = models.TextField()  # Could represent lesson content or material

    def __str__(self):
        return self.title  # Or any other field you want to represent
