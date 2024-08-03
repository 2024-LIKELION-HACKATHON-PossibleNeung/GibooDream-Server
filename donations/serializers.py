from rest_framework import serializers
from .models import *
from users.models import *
import datetime

User = get_user_model()

class BasketItemDreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket_Item_dream
        fields = '__all__'

class CheeringSerializer(serializers.ModelSerializer) :
    user_nickname = serializers.CharField(source='user_email.nickname', read_only=True)# 사용자 이름을 가져오기 위해

    class Meta:
        model = Cheering
        fields = ['user_email','user_nickname', 'basket_heart', 'basket_dream', 'cheering_cont']
        read_only_fields = ['user_email','user_nickname']


class DonationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation_Item
        fields = ['id', 'goods_id', 'basket_item_dream', 'quantity']

class CopyOfDonationSerializer(serializers.ModelSerializer):
    selected_items = serializers.ListField(write_only=True)
    goods_total_price = serializers.IntegerField(read_only=True)
    donation_items = serializers.SerializerMethodField()

    class Meta:
        model = CopyOfDonation
        fields = ['id', 'basket_dream', 'basket_heart', 'goods_total_price', 'buy_date', 'payment', 'receipt_yn', 'selected_items', 'donation_items']

    def get_donation_items(self, obj):
        return DonationItemSerializer(obj.donation_item_set.all(), many=True).data

    def validate(self, data):
        for item in data['selected_items']:
            try:
                basket_item = Basket_Item_dream.objects.get(pk=item['basket_item_dream'])
            except Basket_Item_dream.DoesNotExist:
                raise serializers.ValidationError(f"Basket item dream with id {item['basket_item_dream']} does not exist.")
            
            goods = Goods.objects.get(pk=basket_item.goods_id.id)
            
            if item['quantity'] > basket_item.buy_num:
                raise serializers.ValidationError(f"Requested quantity for {basket_item.goods_id.goods_name} exceeds the required quantity.")
            if item['quantity'] > goods.goods_num:
                raise serializers.ValidationError(f"Requested quantity for {basket_item.goods_id.goods_name} exceeds the available stock.")
        return data

    def create(self, validated_data):
        selected_items_data = validated_data.pop('selected_items')
        user = self.context['request'].user
        donation = CopyOfDonation.objects.create(user_id=user, **validated_data)
        goods_total_price = 0

        for item_data in selected_items_data:
            basket_item = Basket_Item_dream.objects.get(pk=item_data['basket_item_dream'])
            goods = Goods.objects.get(pk=basket_item.goods_id.id)
            quantity = item_data['quantity']
            price = goods.goods_price * quantity
            
            Donation_Item.objects.create(donation_id=donation, goods_id=goods, basket_item_dream=basket_item, quantity=quantity)
            goods.goods_num -= quantity
            goods.save()
            
            basket_item.buy_num -= quantity
            if basket_item.buy_num == 0:
                basket_item.complete = True
            basket_item.save()
            
            goods_total_price += price

        donation.goods_total_price = goods_total_price
        donation.save()

        return donation
    
class DonationItemDetailSerializer(serializers.ModelSerializer):
    donation_item_id = serializers.IntegerField(source='id')
    price = serializers.SerializerMethodField()

    class Meta:
        model = Donation_Item
        fields = ['donation_item_id', 'goods_id', 'basket_item_dream', 'quantity', 'price']

    def get_price(self, obj):
        return obj.goods_id.goods_price * obj.quantity
    
class CopyOfDonationDetailSerializer(serializers.ModelSerializer):
    donation_id = serializers.IntegerField(source='id')
    donation_items = serializers.SerializerMethodField()

    class Meta:
        model = CopyOfDonation
        fields = ['donation_id', 'basket_heart', 'goods_total_price', 'buy_date', 'receipt_yn', 'donation_items']

    def get_donation_items(self, obj):
        items = Donation_Item.objects.filter(donation_id=obj.id)
        return DonationItemDetailSerializer(items, many=True).data

class UserDonationSerializer(serializers.ModelSerializer):
    donations = serializers.SerializerMethodField()
    donate_total = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ['email', 'donate_total', 'donations']

    def get_donations(self, obj):
        donations = CopyOfDonation.objects.filter(user_id=obj)
        return CopyOfDonationDetailSerializer(donations, many=True).data

    def get_donate_total(self, obj):
        donations = CopyOfDonation.objects.filter(user_id=obj)
        total = sum(donation.goods_total_price for donation in donations)
        return total
    

class ReviewSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user_id.nickname', read_only=True)
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['review_id', 'user_nickname', 'donation_id', 'review_cont', 'review_img', 'created_at']

    def get_created_at(self, obj):
        return datetime.datetime.now() if obj._state.adding else obj.created_at

    def create(self, validated_data):
        user = self.context['request'].user
        donation_id = validated_data.pop('donation_id')
        donation = CopyOfDonation.objects.get(id=donation_id)

        if donation.basket_dream and donation.basket_dream.user_id != user:
            raise serializers.ValidationError("You can only review donations you have received.")
        if donation.basket_heart and donation.basket_heart.user_id != user:
            raise serializers.ValidationError("You can only review donations you have received.")

        review = Review.objects.create(user_id=user, donation_id=donation, **validated_data)  # CopyOfDonation 객체를 직접 할당합니다.
        return review
    
