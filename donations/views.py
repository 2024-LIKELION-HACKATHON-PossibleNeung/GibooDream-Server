from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from django.db import transaction



class CheeringView(APIView):
    permission_classes = [IsAuthenticated]  # 로그인된 사용자만 접근 가능

    def post(self, request, *args, **kwargs):
        # 요청 데이터에서 user_id를 가져옵니다
        # user_id는 나중에 커스텀 하면 요청데이터에서 가져오는 것이 아닌 로그인 중인 사용자의 아이디를 가져오는 것으로 변경 필요
        user = request.user
        basket_heart_id = request.data.get('basket_heart')
        basket_dream_id = request.data.get('basket_dream')

        def get_basket(basket_id, basket_type):
            try:
                if basket_type == 'dream':
                    return Basket_dream.objects.get(id=basket_id)
                elif basket_type == 'heart':
                    return Basket_heart.objects.get(id=basket_id)
                else:
                    raise Http404("Invalid basket type")
            except Basket_dream.DoesNotExist:
                pass
            except Basket_heart.DoesNotExist:
                raise Http404("Basket not found")
        
        # basket_id를 기반으로 객체를 가져온다
        basket = None
        if basket_heart_id:
            basket = get_basket(basket_heart_id, 'heart')
        elif basket_dream_id:
            basket = get_basket(basket_dream_id, 'dream')
        else:
            return Response({"error": "Either 'basket_heart' or 'basket_dream' must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        # 시리얼라이저에 사용자와 바구니 정보를 포함한 데이터를 설정합니다
        serializer_data = {
            'basket_heart': basket.basket_heart if isinstance(basket, Basket_heart) else None,
            'basket_dream': basket.basket_dream if isinstance(basket, Basket_dream) else None,
            'cheering_cont': request.data.get('cheering_cont')
        }
        serializer = CheeringSerializer(data=serializer_data)

        if serializer.is_valid():
            cheering_instance = serializer.save(user_email=user)
            return Response(CheeringSerializer(cheering_instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DonationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = UserDonationSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = CopyOfDonationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            donation = serializer.save()
            response_data = {
                'donation_id': donation.id,
                'user_id': donation.user_id.email,  # 여기에서 user의 email을 반환
                'basket_dream': donation.basket_dream.id if donation.basket_dream else None,
                'basket_heart': donation.basket_heart.id if donation.basket_heart else None,
                'goods_total_price': donation.goods_total_price,
                'buy_date': donation.buy_date,
                'receipt_yn': donation.receipt_yn,
                'donation_items': [
                    {
                        'donation_item_id': item.id,
                        'basket_item_dream': item.basket_item_dream.id,
                        'goods_id': item.goods_id.id,
                        'goods_name': item.goods_id.goods_name,
                        'quantity': item.quantity,
                        'price': item.goods_id.goods_price * item.quantity
                    }
                    for item in donation.donation_item_set.all()
                ]
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            review = serializer.save()
            response_data = {
                'review_id': review.review_id,
                'user_nickname': review.user_id.nickname,
                'donation_id': review.donation_id.id,
                'review_cont': review.review_cont,
                'review_img': review.review_img.url if review.review_img else None,
                'created_at': serializer.get_created_at(review),
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)