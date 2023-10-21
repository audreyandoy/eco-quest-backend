import math
from django.shortcuts import render, get_object_or_404
from .models import EcoTransport, Profile, EcoEducation, EcoMeals
from .serializers import EcoTransportSerializer, ProfileSerializer, EcoEducationSerializer, EcoMealsSerializer
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

# Pre-determined values of total carbon footprint in g CO2-equivalent
CO2E_PLANTBASED_BREAKFAST_GRAMS= 1100
CO2E_PLANTBASED_LUNCH_GRAMS = 980
CO2E_PLANTBASED_DINNER_GRAMS = 1100

CO2E_MEATBASED_BREAKFAST_GRAMS = 2600
CO2E_MEATBASED_LUNCH_GRAMS = 3800
CO2E_MEATBASED_DINNER_GRAMS = 4800

# Eco Education Parameters
NUM_WORDS = 200 # Change to 500 once live
NEW_CONTENT = False  # Generate new content from chatGPT, change to True once live


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
            co2_reduced = round(distance * CO2E_PERMILE_CAR_GRAMS, 2)
        #activity = bus
        else:
            co2_reduced = round(distance * CO2E_PERMILE_BUS_GRAMS, 2)
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
    

#--------------api/eco-transport/<int:userid>-------------
# #supports GET for activities for a single user
# class EcoTransportActivityByUser(generics.ListAPIView):

#     serializer_class = EcoTransportSerializer

#     def get(self, request, user):
#         return EcoTransport.objects.all(user=user)
        


#------------------api/eco-profile------------------------------

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

#------------------api/eco-profile/<int:pk>---------------------------------
#supports GET for single user profile
class SingleProfileView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
 
    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        serialized_profile = self.serializer_class(profile)
        return Response(data=serialized_profile.data, status=status.HTTP_200_OK)

#--------------------------------------------------------------------------

# EcoEducation View
def eco_education_view(request, new_content=False):
    """
    Basic view
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
    GET -   Returns a new ChatGPT generated text for the sent "user_id"
    POST -  Creates a new 5 point entry for the user reading the text,
            if "text", is passed in POST log the text
    """
    # permission_classes = [IsAuthenticated]
    serializer_class = EcoEducationSerializer
    def get(self, request, new_content=NEW_CONTENT, format=None):
        serializer = self.serializer_class(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            print(serializer.validated_data)
        # user_info = Profile.objects.filter(id=self.request.user)
        # print(user_info)
        if new_content:
            print("why calling new content?")
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
    

#=============api/eco-meals==================================
#supports GET and POST for authenticated user.
#for the current user token, return all EcoMeals Activities recorded[GET]
#for the current user, add EcoMeals instance to the database [POST]

class EcoMealsView(generics.ListCreateAPIView):
    serializer_class = EcoMealsSerializer

    def get_queryset(self):
        return EcoMeals.objects.all()

    def perform_create(self, serializer):
        # Saves EcoMeals instance
        user = serializer.validated_data['user']
        eco_breakfast = serializer.validated_data['eco_breakfast']
        eco_lunch = serializer.validated_data['eco_lunch']
        eco_dinner = serializer.validated_data['eco_dinner']
        serializer.save(eco_breakfast=eco_breakfast, eco_lunch=eco_lunch, eco_dinner=eco_dinner)

        co2_reduced = self.get_co2_reduced(self.request.data)
        ecomeals_points = self.get_ecomeals_points(co2_reduced)
        
        # Update EcoMeals instance with co2_reduced and ecomeals_points results
        eco_meals_instance = serializer.instance
        eco_meals_instance.co2_reduced = co2_reduced
        eco_meals_instance.ecomeals_points = ecomeals_points
        eco_meals_instance.save()

        # Update Profile with points from EcoMeals
        self.update_user_profile(user, co2_reduced, ecomeals_points)


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

    def update_user_profile(self, user, user_co2_reduced, user_ecomeals_points):
        profile = Profile.objects.get(user=user)
        profile.total_co2e_reduced += user_co2_reduced
        profile.total_points += user_ecomeals_points
        profile.save()

#=================api/eco-meals/<int:pk>=======================
#supports GET for all EcoMeals associated with the specified primary key

class SingleUserAllEcoMealInstancesView(generics.ListAPIView):
    serializer_class = EcoMealsSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        return EcoMeals.objects.filter(user=user_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True) 

        response_data = {
            'meals': serializer.data
        }

        return Response(response_data, status=200)
    
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

    

