from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EcoTransport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=50)
    distance = models.SmallIntegerField()
    co2_reduced = models.FloatField(null=True, blank=True)
    ecoTransport_points = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.activity
    

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, null=True, blank=True)
    streak = models.SmallIntegerField(null=True, blank=True)
    total_points = models.SmallIntegerField(null=True, blank=True)
    total_co2e_reduced = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
