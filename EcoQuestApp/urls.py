from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('eco-transport', views.EcoTransportView.as_view()),
    path('eco-education', views.EcoEducationView.as_view()),
]