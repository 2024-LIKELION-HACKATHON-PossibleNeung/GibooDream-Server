from rest_framework import serializers
from .models import *

User = get_user_model()

class CheeringSerializer(serializers.ModelSerializer) :
    user_name = serializers.CharField(source='user.username', read_only=True)# 사용자 이름을 가져오기 위해

    class Meta:
        model = Cheering
        fields = ['user_id','user_name', 'basket_id', 'cheering_cont']


class DonationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation_Item
        fields = ['donation_item_id', 'basket_item_id', 'quantity']

class DonationItemDetailSerializer(serializers.ModelSerializer):
    goods_id = serializers.IntegerField(source='basket_item_id.goods.id', read_only=True)
    goods_name = serializers.CharField(source='basket_item_id.goods.goods_name', read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    price = serializers.SerializerMethodField()  #동적계산필드
    donation_item_id = serializers.IntegerField(source='id', read_only=True)  # Alias 'id' as 'donation_id'

    class Meta:
        model = Donation_Item
        fields = ['donation_item_id', 'basket_item_id', 'goods_id', 'goods_name', 'quantity', 'price']
    
    def get_price(self, obj):
        # price를 goods_price와 quantity의 곱으로 계산
        return obj.basket_item_id.goods.goods_price * obj.quantity

class DonationSerializer(serializers.ModelSerializer):
    donation_items = DonationItemDetailSerializer(many=True, read_only=True)
    goods_total_price = serializers.IntegerField(read_only=True)
    donation_id = serializers.IntegerField(source='id', read_only=True)  # Alias 'id' as 'donation_id'

    class Meta:
        model = Donation
        fields = ['donation_id', 'user_id', 'basket_id', 'goods_total_price', 'buy_date', 'receipt_yn', 'donation_items']


#기부내역, 기부항목 
class DonationListSerializer(serializers.Serializer):
    user_id=serializers.IntegerField()
    donate_total = serializers.IntegerField()
    donations = DonationSerializer(many=True)