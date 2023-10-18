from django.contrib import admin
from .models import EcoTransport, Profile, EcoEducation

# Register your models here.
admin.site.register(EcoTransport)
admin.site.register(Profile)
admin.site.register(EcoEducation)