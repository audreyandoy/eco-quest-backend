from rest_framework import serializers
from .models import EcoTransport, Profile
from django.contrib.auth.models import User, Group

class EcoTransportSerializer(serializers.ModelSerializer):
    co2_reduced = serializers.ReadOnlyField()
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
        model = EcoTransport
        fields = "__all__"