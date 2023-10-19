from rest_framework import serializers
from ..models import EcoMeals


class EcoMealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcoMeals
        fields = "__all__"
