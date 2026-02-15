from django.db import models
from django.conf import settings

class Application(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE)
    seeker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_applied = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    cover_letter = models.TextField()

    def __str__(self):
        return f"{self.seeker.username} - {self.job.title}"
