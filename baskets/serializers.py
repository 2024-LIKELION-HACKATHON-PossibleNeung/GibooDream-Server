from rest_framework import serializers
from donations.models import *

class DreamBasketSerializer(serializers.ModelSerializer):
  class Meta:
    model = Basket_dream
    fields = '__all__'

class HeartBasketSerializer(serializers.ModelSerializer):
  class Meta:
    model = Basket_heart
    fields = '__all__'

class BasketItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = Basket_Item_dream
    fields='__all__'

