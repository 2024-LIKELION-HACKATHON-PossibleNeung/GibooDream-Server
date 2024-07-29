from django.contrib import admin
from .models import *

class GoodsAdmin(admin.ModelAdmin):
    list_display = ('goods_name', 'goods_price', 'goods_num')  # 관리자 페이지에서 보여줄 필드

admin.site.register(Goods, GoodsAdmin)

admin.site.register(Basket)
admin.site.register(Basket_Item)
admin.site.register(Donation)
admin.site.register(Donation_Item)
admin.site.register(Review)
admin.site.register(Cheering)