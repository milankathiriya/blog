from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title[:30] + '...'

    def save(self):
        super().save()
        img = Image.open(self.image.path)

        if img.width > 1200 or img.height > 700:
            op_size = (1200, 700)
            img.thumbnail(op_size)
            img.save(self.image.path)