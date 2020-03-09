from django.db import models

# Create your models here.
class PlantTip(models.Model):
    tipTitle = models.CharField(max_length=30, null=False, blank=False, unique=False)
    tipText = models.TextField(max_length=500, null=False, blank=False, unique=False)

    def __str__(self):
        return self.tipTitle
