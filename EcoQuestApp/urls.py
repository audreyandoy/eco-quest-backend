from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('eco-transport', views.EcoTransportView.as_view()),
    path('eco-transport/<int:pk>', views.SingleEcoTransportActivityView.as_view()),
    path('eco-profile/<int:pk>', views.SingleProfileView.as_view()),
    path('eco-profile', views.ProfilesView.as_view()),
    # path('eco-education', views.EcoEducationView.as_view()),
    path('eco-education', views.eco_education_view),
    
]