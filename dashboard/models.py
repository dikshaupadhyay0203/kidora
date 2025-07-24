from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ('bug', 'Bug Report'),
        ('suggestion', 'Suggestion'),
        ('compliment', 'Compliment'),
        ('complaint', 'Complaint'),
    ]

    subject = models.CharField(max_length=200)
    message = models.TextField()
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    submitted_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject} by {self.user.username}"
    

    