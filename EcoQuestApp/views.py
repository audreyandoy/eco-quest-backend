import math
from django.shortcuts import render, get_object_or_404
from .models import EcoTransport, Profile, EcoEducation
from .serializers import EcoTransportSerializer, ProfileSerializer, EcoEducationSerializer
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
#from django.contrib.auth.models import User, Group
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


# EcoTransport Feature
#--------------api/eco-transport----------------
#supports GET and POST 
#Returns all EcoTransport Activities recorded for all users[GET]
#Supports recording of an activity to the DB [POST]
class EcoTransportView(generics.ListCreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = EcoTransport.objects.all()
    serializer_class = EcoTransportSerializer
  
    def get_queryset(self):
        return EcoTransport.objects.all()
    
    #calculate carbon footprint and points and save them as part of the record   
    def perform_create(self, serializer):
        activity = serializer.validated_data['activity']
        distance = serializer.validated_data['distance']
        user = serializer.validated_data['user']
        if activity == "walk" or activity == "bicyle":
            co2_reduced = distance * CO2E_PERMILE_CAR_GRAMS
        #activity = bus
        else:
            co2_reduced = distance * CO2E_PERMILE_BUS_GRAMS
        #for every 100g of co2 reduced, award 50 points
        ecoTransport_points =math.floor(co2_reduced/100 * POINTS_AWARDED_100GCO2)
        serializer.save(transport_co2_reduced= co2_reduced, ecoTransport_points=ecoTransport_points)

        #once activity is recorded, update total_points and total_co2e_reduced 
        # in the profile table for this user

        profile = get_object_or_404(Profile, username = user)
        profile.total_points += ecoTransport_points
        profile.total_co2e_reduced += co2_reduced 
        profile.save()

#---------------api/eco-transport/<int:pk>-----------
#supports GET for single Eco transport activity

class SingleEcoTransportActivityView(APIView):

    #permission_classes = [IsAuthenticated]
    serializer_class = EcoTransportSerializer

    def get(self, request, pk):
        activity = get_object_or_404(EcoTransport, pk=pk)
        serialized_activity =  self.serializer_class(activity)
        return Response(data=serialized_activity.data, status=status.HTTP_200_OK)

#------------------api/eco-profile----------------------------

#supports GET and POST 
#Returns all Profiles[GET]
#Supports creating and saving a profile to the DB [POST]

class ProfilesView(generics.ListCreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
  
    def get_queryset(self):
        return Profile.objects.all() 
    
    def post(self, request):
        deserialized_profile = self.serializer_class(data=request.data)
        if deserialized_profile.is_valid():
            deserialized_profile.save()
            return Response(data=deserialized_profile.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": deserialized_profile.errors}, status=status.HTTP_400_BAD_REQUEST)
  




#---------api/eco-profile/<int:pk>-----------
#supports GET for single user profile
class SingleProfileView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
 
    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        serialized_profile = self.serializer_class(profile)
        return Response(data=serialized_profile.data, status=status.HTTP_200_OK)



# Profile View
# TODO this doesn't seem to be working....
# class EcoProfileView(generics.RetrieveAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     lookup_field = 'user__username'

#     def get_queryset(self):
#         user = self.request.user
#         print(Profile.objects.all().filter(user=user))
#         return Profile.objects.all().filter(user=user)

# EcoEducation View
def eco_education_view(request, new_content=False):
    if new_content:
        text = generate_custom_content(save_output=False, display_output=True)
    else:
        response = provide_example_gpt_response()
        text = response["choices"][0]["message"]["content"].strip()
    return HttpResponse(text)


# TODO need to convert to a View class below
# GET to retrieve the ChatGPT text, requires userid of some sort
# POST to post points to the database 5 points / read, requires userid & text read?
class EcoEducationView(generics.ListCreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = EcoEducation.objects.all()
    serializer_class = EcoEducationSerializer

    # filter the queryset by current user
    def get_queryset(self):
        return EcoEducation.objects.all()

    # Need to update this section
    # def perform_create(self, serializer):
    #     activity = serializer.validated_data['activity']
    #     distance = serializer.validated_data['distance']
    #     if activity == "walk" or activity == "bicyle":
    #         co2_reduced = distance * CO2E_PERMILE_CAR_GRAMS
    #     # activity = bus
    #     else:
    #         co2_reduced = distance * CO2E_PERMILE_BUS_GRAMS
    #     # for every 100g of co2 reduced, award 50 points
    #     ecoTransport_points = math.floor(co2_reduced / 100 * POINTS_AWARDED_100GCO2)
    #     serializer.save(co2_reduced=co2_reduced, ecoTransport_points=ecoTransport_points)