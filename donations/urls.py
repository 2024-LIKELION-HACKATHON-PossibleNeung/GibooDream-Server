from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('cheering/', CheeringView.as_view(), name="cheering"),
    path('donations/', DonationView.as_view(), name = "donation"),
    path('donations/<int:user_id>/', DonationListView.as_view(), name='donation-list'),
]