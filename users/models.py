from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=30, blank=True, null=True)
    password = models.CharField(max_length=255)
    username = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

class UserGlobal(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=30, blank=True, null=True)
    spam = models.IntegerField(default=0)
    def increment_spam_count(self):
        self.spam += 1
        self.save()

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.CharField(max_length=30, blank=True, null=True)
