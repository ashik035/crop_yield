from django.db import models
# Create your models here.
class Production(models.Model):
    Division_Name = models.CharField(max_length=120, null=True, blank=True)
    District_Name = models.CharField(max_length=120, null=True, blank=True)
    Crop_Year = models.CharField(max_length=120,null=True, blank=True)
    Season = models.CharField(max_length=120, null=True, blank=True)
    Crop = models.CharField(max_length=120, null=True, blank=True)
    Area = models.CharField(max_length=120, null=True, blank=True)
    Production = models.CharField(max_length=120, null=True, blank=True)

class Recomendation(models.Model):
    N = models.CharField(max_length=120, null=True, blank=True)
    P = models.CharField(max_length=120, null=True, blank=True)
    K = models.CharField(max_length=120, null=True, blank=True)
    temperature = models.CharField(max_length=120, null=True, blank=True)
    humidity = models.CharField(max_length=120, null=True, blank=True)
    ph = models.CharField(max_length=120, null=True, blank=True)
    rainfall = models.CharField(max_length=120, null=True, blank=True)
    label = models.CharField(max_length=120, null=True, blank=True)








