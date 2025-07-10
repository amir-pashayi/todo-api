from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class Task(models.Model):
    FLAG_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flag = models.CharField(max_length=6, choices=FLAG_CHOICES)
    category = models.ForeignKey(Category, related_name='tasks', on_delete=models.CASCADE, blank=True, null=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} - {self.user.username}'

    def clean(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError('End date must be before start date')