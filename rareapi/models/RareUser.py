"""Rare User model module"""
from django.db import models
from django.contrib.auth.models import User

class RareUser (models.Model):
    """Rare User database model"""
    bio = models.CharField(max_length=75)
    profile_image_url = models.CharField(max_length=75)
    created_on = models.DateField()
    active = models.BooleanField()
    user = models.OneToOneField(User, on_delete = models.CASCADE)


