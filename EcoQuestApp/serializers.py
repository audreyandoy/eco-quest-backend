from rest_framework import serializers
from .models import EcoTransport, Profile, EcoMeals, EcoEducation

class EcoTransportSerializer(serializers.ModelSerializer):
    transport_co2_reduced = serializers.ReadOnlyField()
    ecoTransport_points =  serializers.ReadOnlyField()
    activity_date = serializers.ReadOnlyField()
    
    class Meta:
        model = EcoTransport
        fields = "__all__"

 
class ProfileSerializer(serializers.ModelSerializer):
    total_co2e_reduced = serializers.ReadOnlyField()
    total_points =  serializers.ReadOnlyField()
    streak = serializers.ReadOnlyField()
    class Meta:
        model = Profile
        fields = "__all__"


class EcoEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcoEducation
        fields = "__all__"


class EcoMealsSerializer(serializers.ModelSerializer):
    meal_type = serializers.SerializerMethodField()

    def get_meal_type(self, instance):
        if instance.eco_breakfast:
            return "Breakfast"
        elif instance.eco_lunch:
            return "Lunch"
        elif instance.eco_dinner:
            return "Dinner"
        
    class Meta:
        model = EcoMeals
        fields = ("co2_reduced", "ecomeals_points", "entry_date", "meal_type")

