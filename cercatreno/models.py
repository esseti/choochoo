from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Greeting(models.Model):
    author = models.OneToOneField(User)
    content = models.CharField(max_length=100, default='')