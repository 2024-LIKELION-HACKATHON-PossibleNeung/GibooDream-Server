from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("basket/", ApplyBasket.as_view()),
    path("basket/<int:basket_id>/", BasketDetail.as_view()),
    path("baskets/", BasketList.as_view()),
    path("basketStatus/", MyBasketStatus.as_view()),
    path('crawl/', Crawl_items_search.as_view())
]
