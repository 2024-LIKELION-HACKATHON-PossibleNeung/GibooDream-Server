from rest_framework import serializers
from donations.models import *
from users.models import *

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

class DreamBasketStatusSerializer(serializers.ModelSerializer):
  basket_type = serializers.CharField(default="꿈바구니")
  benefit_name = serializers.SerializerMethodField()

  class Meta:
    model = Basket_dream
    fields = ['dbasket_apply', 'dstatus','basket_type', 'benefit_name']

  def get_benefit_name(self, obj):
        try:
            beneficiary = MyUser.objects.get(email=obj.user_id)
            return beneficiary.nickname
        except Beneficiary.DoesNotExist:
            return None
        
class HeartBasketStatusSerializer(serializers.ModelSerializer):
  basket_type = serializers.CharField(default="따숨바구니")
  benefit_name = serializers.SerializerMethodField()

  class Meta:
    model = Basket_heart
    fields = ['hbasket_apply', 'hstatus', 'basket_type', 'benefit_name']
    
  def get_benefit_name(self, obj):
        try:
            beneficiary = MyUser.objects.get(email=obj.user_id)
            return beneficiary.nickname
        except Beneficiary.DoesNotExist:
            return None

