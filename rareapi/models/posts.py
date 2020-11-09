"""Posts model module"""
from django.db import models


class Posts(models.Model):
    """Post database model"""
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    category_id = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    publication_date = models.DateField(auto_now=False, auto_now_add=False)
    image_url = models.CharField(max_length=100)
    content = models.CharField(max_length=200)
    approved = models.BooleanField()