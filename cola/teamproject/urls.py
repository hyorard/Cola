from django.urls import path
from . import views

urlpatterns = [
    path('teamproject/',views.teamproject, name="teamproject"),  
]