from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    career = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='student_photos/')

    def __str__(self):
        return f"{self.first_name} {self.name}"
