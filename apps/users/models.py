from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
  account_approved = models.BooleanField(default=False)
  team_member = models.ForeignKey('self',on_delete=models.SET_NULL, blank=True, null=True, related_name='children')

   