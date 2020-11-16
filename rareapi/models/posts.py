"""Posts model module"""
from django.db import models


class Posts(models.Model):
    """Post database model"""
    rare_user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    publication_date = models.DateField(auto_now=False, auto_now_add=False)
    image_url = models.CharField(max_length=100)
    content = models.CharField(max_length=200)
    approved = models.BooleanField()

    @property
    def IsAuthor(self):
        return self.__IsAuthor

    @IsAuthor.setter
    def IsAuthor(self, value):
        self.__IsAuthor = value

    @property
    def reactions(self):
        return self.__reactions
    
    @reactions.setter
    def reactions(self, value):
        self.__reactions = value