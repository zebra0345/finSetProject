from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from finSetApp.models import DepositProducts, SavingProducts
# Create your models here.

# custom user
class User(AbstractUser):
    pass

class Profile(models.Model):
    User  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    deposit = models.ManyToManyField(DepositProducts, related_name='deposit', null=True, blank=True)
    saving = models.ManyToManyField(SavingProducts, related_name='saving', null=True, blank=True)
    nickName = models.TextField(blank=True, null=True)
