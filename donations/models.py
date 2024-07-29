from django.db import models
from django.contrib.auth import get_user_model

from django.conf import settings


# Create your models here.

###임의 모델###
class Goods(models.Model) :
    goods_price = models.IntegerField(verbose_name="물품 가격",null=False)
    goods_name = models.CharField(verbose_name="물품 이름",max_length=40,null=False)
    goods_num = models.IntegerField(verbose_name="물품 재고",null=False)

class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    buy_num = models.IntegerField(verbose_name= "구매갯수", default=0)
    buy_reason = models.CharField(max_length=300, verbose_name="구매 이유", null=False,default='')
    basket_post = models.DateField(verbose_name="꿈바구니 등록 날짜",auto_now_add=True, null=True) 
    #null = True는 나중에 변경
    basket_complete = models.DateField(verbose_name="꿈바구니 완료 날짜",auto_now_add=False,null=True)
    complete = models.BooleanField(verbose_name="후원 완료 여부", default= False)

class Basket_Item(models.Model):
    basket = models.ForeignKey(Basket, related_name='items', on_delete=models.CASCADE,null=False)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE,null=True)
    #null = True 나중에 변경
    buy_num = models.IntegerField(verbose_name="물품 수량",null=False,default=0)
    price = models.IntegerField(verbose_name="총 가격",default=0)

####



class Donation(models.Model) :
    # Basket 모델 필요!
    basket_id = models.ForeignKey(Basket,verbose_name="꿈바구니 고유번호", null=False, on_delete=models.CASCADE)
    # User 모델 필요! 
    # 일단 auth_user_model로 지정 후 참조!
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="회원 아이디", null=True, on_delete=models.CASCADE)
    goods_total_price = models.IntegerField('물품 총 가격')
    buy_date = models.DateTimeField(verbose_name="구매 일자",auto_now_add=True)
    payment = models.CharField(verbose_name="결제 방법",max_length=100)
    receipt_yn = models.BooleanField(verbose_name="영수증 발급 여부",default = False)

class Donation_Item(models.Model) :
    donation_id = models.ForeignKey(Donation, verbose_name="기부드림 고유번호",null = False, on_delete=models.CASCADE, related_name='donation_items')
    # Basket_Item 모델 필요!
    basket_item_id = models.ForeignKey(Basket_Item, verbose_name="꿈바구니 물품", on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="물품 수량")


class Review(models.Model) :
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="회원 아이디", null=True, on_delete=models.CASCADE)
    donation_id = models.ForeignKey(Donation, verbose_name="기부드림 고유번호",null = False, on_delete=models.CASCADE )
    review_cont = models.CharField(verbose_name="후기 내용", max_length=300)
    review_img = models.ImageField(verbose_name="후기 이미지")

class Cheering(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="회원 아이디", null=True, on_delete=models.CASCADE)
    basket_id = models.ForeignKey(Basket,verbose_name="꿈바구니 고유번호", null=False, on_delete=models.CASCADE)
    cheering_cont = models.CharField(verbose_name = "응원 문구", max_length= 30)




    
