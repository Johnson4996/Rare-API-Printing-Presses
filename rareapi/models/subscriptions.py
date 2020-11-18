"""Comment Model Module"""
from django.db import models

class Subscriptions(models.Model):
    """Subscriptions database model"""
    created_on = models.DateTimeField(auto_now=False, auto_now_add=False)
    ended_on = models.DateTimeField(null=True)
    follower = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="rare_user_follower")
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="rare_user_author")