from rest_framework import serializers
from .models import EcoTransport, Profile
from django.contrib.auth.models import User, Group

class EcoTransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcoTransport
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

