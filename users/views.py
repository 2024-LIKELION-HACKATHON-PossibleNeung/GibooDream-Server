from django.shortcuts import render
from .serializers import UserSerializer
from .models import *
from rest_framework import generics

class UserCreate(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer