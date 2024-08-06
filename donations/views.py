from django.shortcuts import render,  redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser
from .forms import ReviewForm
from rest_framework import generics




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
                    return Basket_dream.objects.get(basket_dream=basket_id)
                elif basket_type == 'heart':
                    return Basket_heart.objects.get(basket_heart=basket_id)
                else:
                    raise Http404("Invalid basket type")
            except Basket_dream.DoesNotExist:
                raise Http404("바구니 아이디가 적절하지 않아요")
            except Basket_heart.DoesNotExist:
                raise Http404("바구니 아이디가 적절하지 않아요")
        
        # basket_id를 기반으로 객체를 가져온다
        basket = None
        if basket_heart_id:
            basket = get_basket(basket_heart_id, 'heart')
        elif basket_dream_id:
            basket = get_basket(basket_dream_id, 'dream')
        else:
            return Response({"error": "따숨바구니, 꿈바구니 중 하나를 알려주세요"}, status=status.HTTP_400_BAD_REQUEST)

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

            user = request.user
            user.donate_total = self.calculate_donate_total(user)
            user.save()

            response_data = {
                'donation_id': donation.id,
                'user_id': donation.user_id.email,  # 여기에서 user의 email을 반환
                'basket_dream': donation.basket_dream.basket_dream if donation.basket_dream else None,
                'basket_heart': donation.basket_heart.basket_heart if donation.basket_heart else None,
                'goods_total_price': donation.goods_total_price,
                'buy_date': donation.buy_date,
                'receipt_yn': donation.receipt_yn,
                'donation_items': [
                    {
                        'donation_item_id': item.id,
                        'basket_item_dream': item.basket_item_dream.id,
                        'goods_name': item.goods_name,
                        'quantity': item.quantity,
                        'price': item.goods_price * item.quantity,
                        'item_url': item.item_url
                    }
                    for item in donation.donation_item_set.all()
                ]
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def calculate_donate_total(self, user):
        donations = CopyOfDonation.objects.filter(user_id=user)
        total = sum(donation.goods_total_price for donation in donations)
        return total
    

class ReviewView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            review = serializer.save()
            response_data = {
                'review_id': review.review_id,
                'user_nickname': review.user_id.nickname,
                'donation_id': review.donation_id.id if review.donation_id else None,
                'review_cont': review.review_cont,
                'review_img': review.review_img.url if review.review_img else None,
                'created_at': serializer.get_created_at(review),
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def review_create_view(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user_id = request.user  # 현재 로그인한 사용자 설정
            donation = form.cleaned_data.get('donation_id')
            
            if donation:
            # 수혜자를 basket_dream 또는 basket_heart를 통해 확인
                if donation.basket_dream and donation.basket_dream.user_id != request.user:
                    form.add_error('donation_id', "You can only review donations you have received.")
                elif donation.basket_heart and donation.basket_heart.user_id != request.user:
                    form.add_error('donation_id', "You can only review donations you have received.")
                else:
                    review.donation_id = donation  # 여기를 수정합니다.
                
            if not form.errors:
                review.save()
                return redirect('review-success')  # 성공 후 리디렉션할 URL 설정

    else:
        form = ReviewForm()
    
    return render(request, 'review_form.html', {'form': form})

def review_success_view(request):
    return render(request, 'review_success.html')



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request) :
        user = request.user
        serializers = UserProfileSerializer(user)
        return Response(serializers.data, status=status.HTTP_200_OK)


class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewListSerializer

    def get_queryset(self):
        queryset = Review.objects.all()
        review_id = self.request.query_params.get('review_id', None)
        if review_id is not None:
            queryset = queryset.filter(review_id = review_id)
        return queryset
