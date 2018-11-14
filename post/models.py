from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from PIL import Image
import os
from datetime import datetime

# Create your models here.


# create token when new user added in database
@receiver(signals.post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def uploadImage(instance, filename):
    date = datetime.now().strftime('%d-%m-%Y')
    time = datetime.now().strftime('%H-%M-%S')
    return f'{date}/{instance.author}/{time}+__+{filename}'


class Post(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to=uploadImage, null=True, blank=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title[:30] + '...'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        
        if img.width > 1200 or img.height > 700:
            op_size = (1200, 700)
            img.thumbnail(op_size)
            img.save(self.image.path)


@receiver(signals.post_delete, sender=Post)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    instance.image.delete(False) 


@receiver(signals.pre_save, sender=Post)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_image = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    new_image = instance.image
    if not old_image == new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)