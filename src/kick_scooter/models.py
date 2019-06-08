from django.db import models

# Create your models here.
class KickScooters(models.Model):
   title       = models.CharField(max_length=120)
   stock       = models.IntegerField(blank=False)
   feature_1   = models.CharField(max_length=220, null=True, blank=True)
   feature_2   = models.CharField(max_length=220, null=True, blank=True)
   feature_3   = models.CharField(max_length=220, null=True, blank=True)
   content     = models.TextField(null=True, blank=True)
   price       = models.DecimalField(max_digits=6, decimal_places=2)