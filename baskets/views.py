from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from .serializers import *
from donations.models import *
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.http import JsonResponse
from .crawler import *
from django.core import serializers
# Create your views here.

class ApplyBasket(APIView):
  def post(self, request, format=None):
    user = request.user
    if (request.data.get('basket_type')=="dream"):
      serializer_basket_data = {
      'user_id': user.email,
      'dbuy_num': request.data.get('totalNum'),
      'dbuy_reason': request.data.get('content'),
      'basket_dream': request.data.get('basket_dream')}
      serializer = DreamBasketSerializer(data=serializer_basket_data)
      item_list = request.data.get('items')
      for item in item_list:
        serializer_item_data = {
          'basket_dream': request.data.get('basket_dream'),
          'goods_price': item['price'],
          'goods_name': item['pName'],
          'item_url': item['item_url'],
          'buy_num': item['amount'],
          'total_price': item['price'] * item['amount'],
          'complete': False,
        }
        serializer_item = BasketItemSerializer(serializer_item_data)
        if serializer_item.is_valid():
          serializer_item.save()

      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    elif (request.data.get('basket_type')=="heart"):
      item_list = request.data.get('items')
      for item in item_list:
        serializer_item_data = {
          'basket_heart': request.data.get('basket_dream'),
          'goods_price': item['price'],
          'goods_name': item['pName'],
          'item_url': item['item_url'],
          'buy_num': item['amount'],
          'total_price': item['price'] * item['amount'],
          'complete': False,
        }
        serializer_item = BasketItemSerializer(serializer_item_data)
        if serializer_item.is_valid():
          serializer_item.save()
      serializer_data = {
      'user_id': user.email,
      'hbuy_num': request.data.get('totalNum'),
      'hbuy_reason': request.data.get('content'),
      'basket_heart': request.data.get('basket_heart')}
      serializer = HeartBasketSerializer(data=serializer_data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  # def delete(self, request):
  #   basketItem = Basket_Item_dream.objects.get(basket_item_id=request.basket_item_id)
  #   basketItem.delete()
  #   return Response(status=status.HTTP_204_NO_CONTENT)
  
  def put(self, request):
    user = request.user
    basket_type = request.data.get("basket_type")
    if(basket_type=="dream"):
      serializer_data = {
      'user_id': user.email,
      'dbuy_num': request.data.get('totalNum'),
      'dbuy_reason': request.data.get('content'),
      'basket_dream': request.data.get('basket_dream')}
      basket = Basket_dream.objects.get(basket_dream=request.data.get('basket_dream'))
      serializer = DreamBasketSerializer(basket, data=serializer_data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif (request.data.get('basket_type')=="heart"):
        serializer_data = {
        'user_id': user.email,
        'hbuy_num': request.data.get('totalNum'),
        'hbuy_reason': request.data.get('content')}
        basket = Basket_heart.objects.get(basket_heart=request.data.get('basket_heart'))
        serializer = HeartBasketSerializer(basket, data=serializer_data)
        if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  

class BasketDream(APIView): 
  def get(self, request):
    basket = Basket_dream.objects.get(user_id=request.user_id)
    serializer = DreamBasketSerializer(basket)
    return Response(serializer.data)
  
  def put(self, request):
    basket = Basket_dream.objects.get(basket_id=request.basket_id)
    serializer = DreamBasketSerializer(basket, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  # def delete(self, request):
  #   basket = Basket_dream.objects.get(basket_id=request.basket_id)
  #   basket.delete()
  #   return Response(status=status.HTTP_204_NO_CONTENT)      

class BasketHeart(APIView): 
  def get(self, request):
    basket = Basket_heart.objects.get(user_id=request.user_id)
    serializer = HeartBasketSerializer(basket)
    return Response(serializer.data)
  
  def put(self, request):
    basket = Basket_heart.objects.get(basket_id=request.basket_id)
    serializer = HeartBasketSerializer(basket, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self, request):
    basket = Basket_heart.objects.get(basket_id=request.basket_id)
    basket.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)      


class BasketList(APIView):
  def get(self, request, format=None):
    basket_type=request.query_params.get('basket_type')
    if(basket_type=="dream"):
      baskets = Basket_dream.objects.all()
      serializer = DreamBasketSerializer(baskets, many=True)
    else:
      baskets = Basket_heart.objects.all()
      serializer = HeartBasketSerializer(baskets, many=True)

    return Response(serializer.data)
    
class BasketDetail(APIView):
  def get(self, request, basket_id, format=None):
    basket_type = request.query_params.get('basket_type')
    if basket_type == "dream":
            basket = get_object_or_404(Basket_dream, basket_dream=basket_id)
            serializer = DreamBasketSerializer(basket)
    else:
      basket = get_object_or_404(Basket_heart, basket_heart=basket_id)
      serializer = HeartBasketSerializer(basket)
    return Response(serializer.data)

class MyBasketStatus(APIView):
  def get(self, request, format=None):
    user = request.user
    user_id=user.email
    dream_basket = get_list_or_404(Basket_dream, user_id=user_id)
    heart_basket=get_list_or_404(Basket_heart, user_id=user_id)
    dbasket_serializer = DreamBasketStatusSerializer(dream_basket, many=True)
    hbasket_serializer = HeartBasketStatusSerializer(heart_basket, many=True)
    combined_data = {
            'basket': dbasket_serializer.data,
            'beneficiary': hbasket_serializer.data
        }
    return Response(combined_data)

class Crawl_items(APIView):
  def get(self, request, format=None):
    category=request.query_params.get('category')
    items_list=crawl_items(category)
    serializer_data = items_list
    item_data=GoodsSerializer(serializer_data, many=True)
    return Response({'status': 'success', 'data': item_data.data })

class Crawl_items_search(APIView):
  def get(self, request, format=None):
    search=request.query_params.get('search')
    items_list=crawl_search_items(search)
    serializer_data = items_list
    item_data=GoodsSerializer(serializer_data, many=True)
    return Response({'status': 'success', 'data': item_data.data })




