from django.db import models

class PostReactions(models.Model):

    user = models.ForeignKey("User", on_delete=models.CASCADE)
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)