"""Comment Model Module"""
from django.db import models

class Subscriptions(models.Model):
    """Subscriptions database model"""
    created_on = models.DateTimeField(auto_now=False, auto_now_add=False)
    ended_on = models.DateTimeField(null=True)
    follower = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="rare_user_follower")
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="rare_user_author")

    @property
    def subscribed(self):
        return self.__subscribed

    @subscribed.setter
    def subscribed(self, value):
        self.__subscribed = value