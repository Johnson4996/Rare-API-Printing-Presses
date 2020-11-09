from django.db import models
from django.db.models.fields import related

class Demotion(models.Model):

    action = models.CharField(max_length=50)
    admin = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="rare_admin")
    approver_one = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="rare_approver")