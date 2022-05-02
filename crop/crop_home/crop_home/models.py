from django.db import models
# Create your models here.
class Production(models.Model):
    Division_Name = models.CharField(max_length=120, null=True, blank=True)
    District_Name = models.CharField(max_length=120, null=True, blank=True)
    Crop_Year = models.IntegerField(null=True, blank=True)
    Season = models.CharField(max_length=120, null=True, blank=True)
    Crop = models.CharField(max_length=120, null=True, blank=True)
    Area = models.IntegerField(max_length=120, null=True, blank=True)
    Production = models.IntegerField(max_length=120, null=True, blank=True)

class Recomendation(models.Model):
    N = models.IntegerField(null=True, blank=True)
    P = models.IntegerField(null=True, blank=True)
    K = models.IntegerField(null=True, blank=True)
    temperature = models.FloatField(max_length=120, null=True, blank=True)
    humidity = models.FloatField(max_length=120, null=True, blank=True)
    ph = models.FloatField(max_length=120, null=True, blank=True)
    rainfall = models.FloatField(max_length=120, null=True, blank=True)
    label = models.CharField(max_length=120, null=True, blank=True)






