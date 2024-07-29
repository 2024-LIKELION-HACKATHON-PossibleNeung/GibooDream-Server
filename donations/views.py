from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny


class CheeringView(APIView):
    permission_classes = [AllowAny]  # 모든 사용자 허용 설정

    def post(self, request, *args, **kwargs):
        # 요청 데이터에서 user_id를 가져옵니다
        # user_id는 나중에 커스텀 하면 요청데이터에서 가져오는 것이 아닌 로그인 중인 사용자의 아이디를 가져오는 것으로 변경 필요
        user_id = request.data.get('user_id') 
        basket_id = request.data.get('basket_id')

        # user_id가 요청 데이터에 포함되어 있는지 확인
        if not user_id:
            return Response({"error": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        # user_id와 basket_id를 기반으로 객체를 가져옵니다
        user = get_object_or_404(User, id=user_id)
        basket = get_object_or_404(Basket, id=basket_id)

        # 시리얼라이저에 사용자와 바구니 정보를 포함한 데이터를 설정합니다
        serializer_data = {
            'user_id': user.id,
            'basket_id': basket.id,
            'cheering_cont': request.data.get('cheering_cont')
        }

        serializer = CheeringSerializer(data=serializer_data)
        if serializer.is_valid():
            cheering = serializer.save()

            # 저장 후 사용자 이름 로깅
            user_name = user.username if user else 'Anonymous'
            print("Saved Cheering with user:", user_name)

            # 응답 데이터에 사용자 이름 추가
            response_data = serializer.data
            response_data['user_name'] = user_name

            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DonationView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        basket_id = request.data.get('basket_id')
        selected_items = request.data.get('selected_items', [])
        payment = request.data.get('payment')
        agree_to_terms = request.data.get('agree_to_terms')
        receipt_yn = request.data.get('receipt_yn')

        if not agree_to_terms:
            return Response({"error": "You must agree to the terms."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        basket = get_object_or_404(Basket, id=basket_id)

        goods_total_price = 0

        # Create Donation object first
        donation = Donation.objects.create(
            basket_id=basket,
            user_id=user,
            goods_total_price=0,  # Placeholder, will update later
            payment=payment,
            receipt_yn=receipt_yn
        )

        for item in selected_items:
            basket_item_id = item.get('basket_item_id')
            quantity = item.get('quantity')

            basket_item = get_object_or_404(Basket_Item, id=basket_item_id)
            goods = basket_item.goods

            if quantity > goods.goods_num:
                return Response({"error": f"Insufficient stock for goods_id {goods.id}."}, status=status.HTTP_400_BAD_REQUEST)
            if quantity > basket_item.buy_num:
                return Response({"error": f"Insufficient quantity in basket_item_id {basket_item_id}."}, status=status.HTTP_400_BAD_REQUEST)

            # Calculate total price
            price = basket_item.price
            goods_total_price += price * quantity

            # Create Donation_Item and set donation_id
            donation_item = Donation_Item.objects.create(
                donation_id=donation,  # Directly set donation_id here
                basket_item_id=basket_item,
                quantity=quantity
            )

            # Update stock and basket item quantity
            goods.goods_num -= quantity
            goods.save()

            basket_item.buy_num -= quantity
            basket_item.save()

        # Update the total price in the Donation object
        donation.goods_total_price = goods_total_price
        donation.save()

        # Retrieve donation with related donation_items
        donation = Donation.objects.prefetch_related('donation_items__basket_item_id__goods').get(id=donation.id)

        # Serialize and return the response
        serializer = DonationSerializer(donation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class DonationListView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, id=user_id)

        #donations 기록 가져오기
        donations = Donation.objects.filter(user_id=user)

        #donate_total 계산하기
        donate_total = donations.aggregate(total=models.Sum('goods_total_price'))['total'] or 0

        serializer = DonationListSerializer({
            'user_id': user_id,
            'donate_total': donate_total,
            'donations': donations
        })

        return Response(serializer.data, status=status.HTTP_200_OK)

