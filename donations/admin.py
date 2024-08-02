from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import *
from .forms import BasketItemDreamForm


class BasketItemDreamAdmin(admin.ModelAdmin):
    form = BasketItemDreamForm
    fields = ['basket_dream', 'basket_heart', 'goods_id', 'buy_num', 'total_price', 'complete']



    def save_model(self, request, obj, form, change):
        if not obj.basket_dream and not obj.basket_heart:
            raise ValidationError("Either 'basket_dream' or 'basket_heart' must be provided.")
        
        if not obj.basket_dream:
            obj.basket_dream = None
        if not obj.basket_heart:
            obj.basket_heart = None
        
        obj.save()

admin.site.register(Basket_Item_dream, BasketItemDreamAdmin)

admin.site.register(Goods)
admin.site.register(Basket_dream)
admin.site.register(Basket_heart)
admin.site.register(CopyOfDonation)
admin.site.register(Donation_List)
admin.site.register(Donation_Item)
admin.site.register(Review)
admin.site.register(Cheering)