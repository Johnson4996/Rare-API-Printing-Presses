"""Rare User model module"""
from django.db import models
from django.contrib.auth.models import User

class RareUser (models.Model):
    """Rare User database model"""
    bio = models.CharField(max_length=75)
    profile_image_url = models.ImageField(upload_to='profile_image_url', height_field=None, max_length=None, width_field=None, null=True)
    created_on = models.DateField()
    active = models.BooleanField()
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    @property
    def IsAdmin(self):
        return self.__IsAdmin

    @IsAdmin.setter
    def IsAdmin(self, value):
        self.__IsAdmin = value

