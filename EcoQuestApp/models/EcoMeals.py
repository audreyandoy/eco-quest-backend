from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EcoMeals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    eco_breakfast = models.BooleanField(default=False)
    eco_lunch = models.BooleanField(default=False)
    eco_dinner = models.BooleanField(default=False)
    co2_reduced = models.FloatField(null=True, blank=True)
    ecomeals_points = models.SmallIntegerField(null=True, blank=True)
    entry_date = models.DateField(db_index = True, auto_now=True)

    def __str__(self):
        return self.activity
    

    
