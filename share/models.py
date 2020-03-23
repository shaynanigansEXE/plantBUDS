from django.db import models

# Create your models here.
class PlantTip(models.Model):
    tipTitle = models.CharField(max_length=30, null=False, blank=False, unique=False)
    tipText = models.TextField(max_length=500, null=False, blank=False, unique=False)

    def __str__(self):
        return self.tipTitle

from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

class PlantBuddy(models.Model):
	def __str__(self):
		return self.user.username

	farm_pro = models.BooleanField(default=False)  # the user is not pro farmer yet
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	created = models.DateField(auto_now=True)   # maybe redundant, user model has date_joined
	updated = models.DateField(auto_now=True)
