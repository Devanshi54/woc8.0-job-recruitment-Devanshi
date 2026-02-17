from django.db import models
from django.conf import settings
from django.utils import timezone
class Application(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE)
    seeker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_applied = models.DateTimeField(auto_now_add=True)
    resume = models.FileField(upload_to='resumes/')
    interview_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    cover_letter = models.TextField(blank=False)

    def __str__(self):
        return f"{self.seeker.username} - {self.job.title}"
class Notification(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
