import math
from django.shortcuts import render, get_object_or_404
from ..models import EcoMeals
from ..serializers import EcoMealsSerializer
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication

# Pre-determined values of total carbon footprint in g CO2-equivalent
CO2E_PLANTBASED_BREAKFAST_GRAMS= 1100
CO2E_PLANTBASED_LUNCH_GRAMS = 980
CO2E_PLANTBASED_DINNER_GRAMS = 1100

CO2E_MEATBASED_BREAKFAST_GRAMS = 2600
CO2E_MEATBASED_LUNCH_GRAMS = 3800
CO2E_MEATBASED_DINNER_GRAMS = 4800

POINTS_AWARDED_100GCO2 =  50

# Create your views here.

#=============api/eco-meals==================================
#supports GET and POST for authenticated user.
#for the current user token, return all EcoMeals Activities recorded[GET]
#for the current user, add EcoMeals instance to the database [POST]

class EcoMealsView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = EcoMealsSerializer

    def get_queryset(self):
        user = self.request.user
        return EcoMeals.objects.filter(user=user)

    def perform_create(self, serializer):
        # Saves EcoMeals instance
        serializer.save(user=self.request.user)

        co2_reduced = self.get_co2_reduced(self.request.data)
        ecomeals_points = self.get_ecomeals_points(co2_reduced)
        
        # Update EcoMeals instance with co2_reduced and ecomeals_points results
        eco_meals_instance = serializer.instance
        eco_meals_instance.co2_reduced = co2_reduced
        eco_meals_instance.ecomeals_points = ecomeals_points
        eco_meals_instance.save()

    def get_co2_reduced(self, user_ecomeals_input):
        co2_reduced = 0

        if user_ecomeals_input['eco_breakfast'] == True:
            co2_reduced = CO2E_MEATBASED_BREAKFAST_GRAMS - CO2E_PLANTBASED_BREAKFAST_GRAMS
        
        elif user_ecomeals_input['eco_lunch'] == True:
            co2_reduced = CO2E_MEATBASED_LUNCH_GRAMS - CO2E_PLANTBASED_LUNCH_GRAMS

        elif user_ecomeals_input['eco_dinner'] == True:
            co2_reduced = CO2E_MEATBASED_DINNER_GRAMS - CO2E_PLANTBASED_DINNER_GRAMS
        
        return co2_reduced

    def get_ecomeals_points(self, user_co2_reduced):
        ecomeals_points = math.floor(user_co2_reduced / 100 * POINTS_AWARDED_100GCO2)

        return ecomeals_points 

    

#=================api/eco-meals/<int:pk>=======================
#supports GET for a single EcoMeals activity for an authenticated user