from django.urls import path
from . import views

urlpatterns = [
    path('eco-transport', views.EcoTransportView.as_view()),
]