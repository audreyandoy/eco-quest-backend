import math
from django.shortcuts import render, get_object_or_404
from .models import EcoTransport, Profile
from .serializers import EcoTransportSerializer, ProfileSerializer
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication
from django.http import HttpResponse


CO2E_PERMILE_CAR_GRAMS = 400
CO2E_PERMILE_BUS_GRAMS = 228
POINTS_AWARDED_100GCO2 =  50


# Create your views here.

# Top Level API
def index(request):
    return HttpResponse("Hello, sustainable world. You're at the EcoApp Top level index.")

# EcoTransport Feature
#supports GET and POST for authenticated user.
#for the current user token, return all EcoTransport Activities recorded[GET]
#for the current user, add activity to the DB [POST]
class EcoTransportView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = EcoTransport.objects.all()
    serializer_class = EcoTransportSerializer

    """ def get(self, request):
        transportList = self.filter_queryset(self.get_queryset())
        serialized_transportList = self.serializer_class(transportList, many=True)
        return Response(data=serialized_transportList.data, status=status.HTTP_200_OK) """
    
    #filter the queryset by current user
    def get_queryset(self):
        return EcoTransport.objects.all().filter(user = self.request.user)
    
    #calculate carbon footprint and points and save them as part of the record   
    def perform_create(self, serializer):
        activity = serializer.validated_data['activity']
        distance = serializer.validated_data['distance']
        if activity == "walk" or activity == "bicyle":
            co2_reduced = distance * CO2E_PERMILE_CAR_GRAMS
        #activity = bus
        else:
            co2_reduced = distance * CO2E_PERMILE_BUS_GRAMS
        #for every 100g of co2 reduced, award 50 points
        ecoTransport_points =math.floor(co2_reduced/100 * POINTS_AWARDED_100GCO2)
        serializer.save(co2_reduced = co2_reduced, ecoTransport_points=ecoTransport_points)


# EcoEducation Feature
class EcoEducationView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        print(Profile.objects.all().filter(user=user))
        return Profile.objects.all().filter(user=user)

    # def EcoEducation(self, request):
    #     return HttpResponse("Hello, sustainable world. You're at the EcoEducation index.")

