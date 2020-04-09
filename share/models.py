from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

#class PlantTip(models.Model):
#    def __str__(self):
#        return self.tipTitle

#    tipTitle = models.CharField(max_length=30, null=False, blank=False, unique=False)
#    tipText = models.TextField(max_length=500, null=False, blank=False, unique=False)

class PlantBuddy(models.Model):
	def __str__(self):
		return self.user.username

	farm_pro = models.BooleanField(default=False)  # the user is not a coder yet
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	created = models.DateField(auto_now=True)   # maybe redundant, user model has date_joined
	updated = models.DateField(auto_now=True)

class Posts(models.Model):
	def __str__(self):
		return self.title
	# FK
	publisher = models.ForeignKey(PlantBuddy, on_delete=models.CASCADE, null=True)

	title = models.CharField(max_length=50, null=False, blank=False, unique=False)
	description = models.TextField(max_length=100, null=False, blank=False, unique=False)
	body = models.TextField(max_length=10000, unique=False)
	make_public = models.BooleanField(default=True)
	image = models.ImageField(upload_to='my_posts/', blank=True)  # add an image for the algorithm or flow chart
	created = models.DateField(auto_now=True)
	updated = models.DateField(auto_now=True)
