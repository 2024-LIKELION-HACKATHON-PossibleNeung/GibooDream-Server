from django.db import models
from django.contrib.auth import get_user_model

from django.conf import settings


# Create your models here.

###Goods###
class Category1(models.Model) :
    category1_div = models.CharField(max_length=10, verbose_name="카테고리1")

class Category2(models.Model) :
    category1_id = models.ForeignKey(Category1, verbose_name="분류1", null = False, on_delete=models.CASCADE)
    category2_div = models.CharField(max_length=10, verbose_name="카테고리2")

class Goods(models.Model) :
    goods_price = models.IntegerField(verbose_name="물품 가격",null=False)
    goods_name = models.CharField(verbose_name="물품 이름",max_length=40,null=False)
    goods_num = models.IntegerField(verbose_name="물품 재고",null=False)
    category1 = models.ForeignKey(Category1, verbose_name="카테고리1", null=False, on_delete=models.CASCADE)
    category2 = models.ForeignKey(Category2,verbose_name="카테고리2", null = False, on_delete= models.CASECADE)
    item_url = models.URLField(max_length=200)
    item_img = models.URLField(max_length=200)
####



class Donation(models.Model) :
    # User 모델 필요! 
    # 일단 auth_user_model로 지정 후 참조!
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="회원 아이디", null=True, on_delete=models.CASCADE)

    # Basket_dream, Basket_heart 모델 필요!
    basket_dream = models.ForeignKey(Basket_dream, verbose_name="꿈바구니 고유번호", null = True, on_delete=models.CASCADE)
    basket_heart = models.ForeignKey(Basket_heart,verbose_name="따숨바구니 고유번호", null=True, on_delete=models.CASCADE)


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

    basket_dream = models.ForeignKey(Basket_dream, verbose_name="꿈바구니 고유번호", null = True, on_delete=models.CASCADE)
    basket_heart = models.ForeignKey(Basket_heart,verbose_name="따숨바구니 고유번호", null=True, on_delete=models.CASCADE)
    
    cheering_cont = models.CharField(verbose_name = "응원 문구", max_length= 30)




    
