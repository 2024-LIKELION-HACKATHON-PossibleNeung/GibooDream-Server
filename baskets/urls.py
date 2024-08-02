from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("basket/", ApplyBasket.as_view()),
    path("baskets/<int:user_id>/", BasketDream.as_view()),
    path("baskets/", BasketList.as_view()),
]
