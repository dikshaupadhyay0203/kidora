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


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    score = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.topic:
            return f"{self.user.username}'s quiz on {self.topic.name}"
        return f"{self.user.username}'s quiz on {self.subject.name}"

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    average_percentage = models.FloatField(default=0.0)
    last_score = models.FloatField(default=0.0)
    suggestion = models.TextField(blank=True, null=True)
    completed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s progress in {self.subject.name}"

    
