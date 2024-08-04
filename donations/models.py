from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

class Goods(models.Model) :

    CATEGORY = [
        ('식료품', [
            ('rice', '쌀'), 
            ('bread', '빵'),
        ]),
        ('청소용품', [
            ('detergent', '세제'),
            ('fabric_softener', '섬유유연제'),
        ]),
        ('주방용품', [
            ('scrubbers', '수세미'),
        ]),
        ('위생용품', [
            ('tissue', '휴지'),
        ]),
        ('사무용품', [
            ('note', '노트'),
        ]),
        ('기타', [
            ('paper-cup', '종이컵'),
        ]),
    ]

    def get_category_choices(category):
        # Flatten the nested structure
        choices = []
        for category, subcategories in category:
            choices.extend(subcategories)
        return choices
 

    goods_id = models.IntegerField(verbose_name="물품 아이디",null=False)
    goods_price = models.IntegerField(verbose_name="물품 가격",null=False)
    goods_name = models.CharField(verbose_name="물품 이름",max_length=40,null=False)
    goods_num = models.IntegerField(verbose_name="물품 재고",null=False)
    item_url=models.CharField(verbose_name="물품 주소",max_length=40,null=False)
    item_img=models.CharField(verbose_name="물품 이미지주소",max_length=40,null=False)
   
class Basket_dream(models.Model):
    basket_dream = models.IntegerField(verbose_name="꿈바구니 아이디",null=False)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dbuy_num = models.IntegerField(verbose_name= "구매갯수", default=0)
    dbuy_reason = models.CharField(max_length=300, verbose_name="구매 이유", null=False,default='')
    dbasket_apply = models.DateField(verbose_name="꿈바구니 신청 날짜",auto_now_add=True, null=True) 
    dbasket_post = models.DateField(verbose_name="꿈바구니 등록 날짜",auto_now_add=True, null=True) 
    dstatus = models.CharField(verbose_name="신청상태", null=False,default='승인대기', max_length=20) 
    dbasket_complete = models.DateField(verbose_name="꿈바구니 완료 날짜",auto_now_add=False,null=True)

class Basket_heart(models.Model):
    basket_heart=models.IntegerField(verbose_name="따숨바구니 고유번호",null=False,default=0)
    user_id=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hbuy_num=models.IntegerField(verbose_name= "구매갯수", default=0)
    hbuy_reason=models.CharField(max_length=300, verbose_name="구매 이유", null=False,default='')
    hbasket_apply=models.DateField(verbose_name="따숨바구니 신청 날짜",auto_now_add=True, null=True) 
    hstatus=models.CharField(verbose_name="신청상태", null=False,default='승인대기',max_length=20) 
    hbasket_post=models.DateField(verbose_name="따숨바구니 등록 날짜",auto_now_add=True, null=True) 
    hbasket_complete=models.DateField(verbose_name="따숨바구니 완료 날짜",auto_now_add=False,null=True)

class Basket_Item_dream(models.Model):
    basket_dream = models.ForeignKey(Basket_dream, on_delete=models.CASCADE,null=True) #null 허용해줘야 함
    basket_heart = models.ForeignKey(Basket_heart, on_delete=models.CASCADE,null=True)
    goods_name = models.CharField(verbose_name="상품명", null = False, max_length=50)
    item_url = models.CharField(verbose_name="상품 url", null = False, max_length = 300)
    buy_num = models.IntegerField(verbose_name="물품 수량",null=False,default=0)
    total_price = models.IntegerField(verbose_name="총 가격",default=0)
    complete=models.BooleanField(default = False)

class CopyOfDonation(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    basket_dream = models.ForeignKey(Basket_dream, on_delete=models.CASCADE, null=True)
    basket_heart = models.ForeignKey(Basket_heart, on_delete=models.CASCADE, null=True)
    goods_total_price = models.IntegerField(verbose_name="물품 총 가격", default=0)
    buy_date = models.DateField(verbose_name="구매일자", auto_now_add=True, null=True)
    payment = models.CharField(verbose_name="결제방법", max_length=20)
    receipt_yn = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

class Donation_List(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    donation_id = models.ForeignKey(CopyOfDonation, on_delete=models.CASCADE)

class Donation_Item(models.Model) :
    donation_id = models.ForeignKey(CopyOfDonation,  on_delete=models.CASCADE)
    goods_id = models.ForeignKey(Goods, on_delete=models.CASCADE)
    basket_item_dream = models.ForeignKey(Basket_Item_dream, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="물품 수량")


class Review(models.Model) :
    review_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="회원 아이디", null=True, on_delete=models.CASCADE)
    donation_id = models.ForeignKey(CopyOfDonation, on_delete=models.CASCADE)
    review_cont = models.CharField(verbose_name="후기 내용", max_length=300)
    review_img = models.ImageField(verbose_name="후기 이미지", upload_to='reviews/')


class Cheering(models.Model):
    cheering_id=models.AutoField(verbose_name="응원메세지 고유번호",null=False, primary_key=True)
    user_email = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="회원 이메일", on_delete=models.CASCADE)
    basket_heart = models.ForeignKey(Basket_heart,verbose_name="따숨바구니 고유번호", null=True, on_delete=models.CASCADE)
    basket_dream = models.ForeignKey(Basket_dream,verbose_name="꿈바구니 고유번호", null=True, on_delete=models.CASCADE)

    cheering_cont = models.CharField(verbose_name = "응원 문구", max_length= 30)

class Beneficiary(models.Model):
    user_id=models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="회원 아이디", null=False, on_delete=models.CASCADE)
    benefit_name=models.CharField(verbose_name = "수혜자이름", max_length= 30)
    address=models.CharField(verbose_name = "수혜자 주소", max_length= 30)
    address_det=models.CharField(verbose_name = "수혜자 세부주소", max_length= 30)
    benefit_ssn=models.CharField(verbose_name = "수혜자 주민등록번호", max_length= 30)
    benefit_file=models.FileField(upload_to="uploads/")



    
