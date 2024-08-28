from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    profile_photo = models.ImageField(_("profile photo"), upload_to='profile_photos/', null=True, blank=True)

    # Add related_name attributes to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Avoids conflict with 'auth.User.groups'
        blank=True,
        help_text=_("Groups this user belongs to."),
        related_query_name='customuser'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Avoids conflict with 'auth.User.user_permissions'
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_query_name='customuser'
    )

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    def __str__(self):
        return self.title
