from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('cheering/', CheeringView.as_view(), name="cheering"),
    path('donations/', DonationView.as_view(), name = "donation"),
    path('reviews/', ReviewView.as_view(), name='review-create'),
]
