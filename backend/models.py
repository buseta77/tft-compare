from django.db import models


# Create your models here.
class UsersCompared(models.Model):
    username1 = models.CharField(max_length=100, blank=False)
    username2 = models.CharField(max_length=100, blank=False)
    server = models.CharField(max_length=50, blank=False)
    compared_at = models.DateTimeField(auto_now_add=True)
