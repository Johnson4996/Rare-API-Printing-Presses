"""Post Tags model module"""
from django.db import models

class PostTag (models.Model):
    """Post Tag database model"""
    post = models.ForeignKey("Posts", on_delete=models.CASCADE)
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)