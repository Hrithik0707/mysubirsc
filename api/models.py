from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser):
    phone_no = models.CharField(max_length = 12, default= 'NONE')

# Create your models here.
