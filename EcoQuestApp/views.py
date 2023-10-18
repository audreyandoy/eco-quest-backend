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
from .chatgpt import provide_example_gpt_response, generate_custom_content


CO2E_PERMILE_CAR_GRAMS = 400
CO2E_PERMILE_BUS_GRAMS = 228
POINTS_AWARDED_100GCO2 =  50


# Create your views here.
# Top Level API Splash Page
def index(request):
    return HttpResponse("Hello, sustainable world. You're at the EcoApp Top level index.")


# Eco-Education view
# TODO need to convert to a View class below
# GET to retrieve the ChatGPT text
# POST to post points to the database 5 points / read.

def eco_education_view(request, new_content=False):
    if new_content:
        text = generate_custom_content(save_output=False, display_output=True)
    else:
        response = provide_example_gpt_response()
        text = response["choices"][0]["message"]["content"].strip()
    return HttpResponse(text)

# EcoTransport Feature
#supports GET and POST for authenticated user.
#for the current user token, return all EcoTransport Activities recorded[GET]
#for the current user, add activity to the DB [POST]
class EcoTransportView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = EcoTransport.objects.all()
    serializer_class = EcoTransportSerializer
  
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

class SingleEcoTransportActivityView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = EcoTransportSerializer

    def get(self, request, pk):
        activity = get_object_or_404(EcoTransport, pk=pk)
        serialized_activity =  self.serializer_class(activity)
        return Response(data=serialized_activity.data, status=status.HTTP_200_OK)


# Profile Query
# TODO this doesn't seem to be working....
class EcoProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user__username'

    def get_queryset(self):
        user = self.request.user
        print(Profile.objects.all().filter(user=user))
        return Profile.objects.all().filter(user=user)
