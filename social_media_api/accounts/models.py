from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    followers = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='following_users',  # Change this name
        blank=True
    )
    following = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='follower_users',  # Change this name
        blank=True
    )