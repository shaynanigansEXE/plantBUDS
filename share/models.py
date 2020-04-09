from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class PlantBuddy(models.Model):
	def __str__(self):
		return self.user.username

	farm_pro = models.BooleanField(default=False)  # the user is not a coder yet
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	created = models.DateField(auto_now=True)   # maybe redundant, user model has date_joined
	updated = models.DateField(auto_now=True)

class Blog(models.Model):
    def __str__(self):
        return self.title
    publisher = models.ForeignKey(PlantBuddy, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False, unique=False)
    description = models.TextField(max_length=100, null=False, blank=False, unique=False)
    subject = models.CharField(max_length=50, null=False, blank=False, unique=False)
    body = models.TextField(max_length=10000, unique=False)
    make_public = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)     # everytime the obj is saved, new time is saved
