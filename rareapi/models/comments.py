"""Comment Model Module"""
from django.db import models

class Comments(models.Model):
    """Comments database model"""
    content = models.CharField(max_length=250)
    subject = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=False)
    post_id = models.ForeignKey("Posts", on_delete=models.CASCADE)
    author_id = models.ForeignKey("Authors", on_delete=models.CASCADE)