"""Comment Model Module"""
from django.db import models

class Subscriptions(models.Model):
    """Subscriptions database model"""
    created_on = models.DateTimeField(auto_now=False, auto_now_add=False)
    ended_on = models.DateTimeField(auto_now=False, auto_now_add=False)
    follower_id = models.ForeignKey("Authors", on_delete=models.CASCADE)
    author_id = models.ForeignKey("Authors", on_delete=models.CASCADE)