from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    is_distribution = models.BooleanField(default=False)
    date_muted = models.DateTimeField(blank=True, null=True)
    date_blocked = models.DateTimeField(blank=True, null=True)