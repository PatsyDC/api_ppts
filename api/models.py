from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    def is_valid(self):
        return self.expires_at > timezone.now()

class Presentation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="presentations")
    description = models.TextField()
    image_before = models.ImageField(upload_to='slides/')
    image_after = models.ImageField(upload_to='slides/')
    fecha = models.DateField()
