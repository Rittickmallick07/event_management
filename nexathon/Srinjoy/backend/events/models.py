from django.db import models
from django.contrib.auth.models import User


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


class Event(models.Model):
    CATEGORY_CHOICES = [
        ("university", "University"),
        ("sports", "Sports"),
        ("conference", "Conference"),
        ("concert", "Concert"),
        ("stage", "Stage Shows"),
        ("webinar", "Webinar"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()  # includes date + time
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.category})"
