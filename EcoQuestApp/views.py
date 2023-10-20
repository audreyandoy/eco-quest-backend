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
  
    #filter the queryset by current user
    def get_queryset(self):
        return EcoTransport.objects.all()
    
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

#-------api/eco-transport/<int:pk>-----------
#supports GET for single Eco transport activity

class SingleEcoTransportActivityView(APIView):

    #permission_classes = [IsAuthenticated]
    serializer_class = EcoTransportSerializer

    def get(self, request, pk):
        activity = get_object_or_404(EcoTransport, pk=pk)
        serialized_activity =  self.serializer_class(activity)
        return Response(data=serialized_activity.data, status=status.HTTP_200_OK)


# Profile View
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


# EcoEducation View
def eco_education_view(request, new_content=False):
    """
    return raw text content from chatgpt
    """
    if new_content:
        text = generate_custom_content(save_output=False, display_output=True)
    else:
        response = provide_example_gpt_response()
        text = response["choices"][0]["message"]["content"].strip()
    return HttpResponse(text)

class EcoEducation(APIView):
    """
    GET -   Returns a new ChatGPT generated text
    POST -  Creates a new 5 point entry for the user reading the text,
            if "text", is passed back it logs the text as well --> may use for future inputs
    """
    permission_classes = [IsAuthenticated]
    serializer_class = EcoEducationSerializer

    def get(self, request, new_content=False, format=None):
        if new_content:
            text = generate_custom_content(max_tokens=200, save_output=False, display_output=True)
        else:
            response = provide_example_gpt_response()
            text = response["choices"][0]["message"]["content"].strip()

        return Response(data={"text": text}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(points=5)
            # Assign 5 points for every passage read
            # want to post text to read what was last?
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
