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
C02E_PLANTBASED_BREAKFAST_GRAMS= 1100
CO2E_PLANTBASED_LUNCH_GRAMS = 980
CO2E_PLANTBASED_DINNER_GRAMS = 1100

CO2E_MEATBASED_BREAKFAST_GRAMS = 2600
CO2E_MEATBASED_LUNCH_GRAMS = 3800
C02E_MEATBASED_DINNER_GRAMS = 4800

POINTS_AWARDED_100GCO2 =  50

# Create your views here.

#=============api/eco-meals==================================
#supports GET and POST for authenticated user.
#for the current user token, return all EcoMeals Activities recorded[GET]
#for the current user, add activity to the DB [POST]

class EcoMealsView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = EcoMealsSerializer

    def get_queryset(self):
        user = self.request.user
        return EcoMeals.objects.filter(user=user)
#=================api/eco-meals/<int:pk>=======================
#supports GET for a single EcoMeals activity for an authenticated user