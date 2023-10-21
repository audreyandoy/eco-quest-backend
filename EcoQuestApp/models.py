from django.db import models
#from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):  # This is a table for rolling up stats on user activity
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True)
    age = models.SmallIntegerField(null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    streak = models.SmallIntegerField(null=True, blank=True)
    total_points = models.SmallIntegerField(default=0)
    total_co2e_reduced = models.FloatField(default=0)
    #  Do we need a 1 month or set period of time rolling average?
    # Also what about total points for each activity?
    def __str__(self):
        return self.username


class EcoTransport(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    activity = models.CharField(max_length=50)
    distance = models.FloatField()
    transport_co2_reduced = models.FloatField(null=True, blank=True)
    ecoTransport_points = models.SmallIntegerField(null=True, blank=True)
    activity_date = models.DateField(db_index = True, auto_now=True)

    def __str__(self):
        return self.activity
    

class EcoEducation(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # activity = models.CharField(max_length=50)  # to be inline with other activities
    points = models.SmallIntegerField(null=True, blank=True)  # 5 points per reading activity
    activity_date = models.DateTimeField(db_index=True, auto_now=True)
    text = models.CharField(max_length=2000, null=True, blank=True)  # store text that was read

    def __str__(self):
        return self.user.username


class EcoMeals(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    eco_breakfast = models.BooleanField(default=False)
    eco_lunch = models.BooleanField(default=False)
    eco_dinner = models.BooleanField(default=False)
    co2_reduced = models.FloatField(null=True, blank=True)
    ecomeals_points = models.SmallIntegerField(null=True, blank=True)
    entry_date = models.DateField(db_index = True, auto_now=True)

    def __str__(self):
        return self.user.username
    
        return self.activity_date
