from django import forms
from .models import Basket_Item_dream

class BasketItemDreamForm(forms.ModelForm):
    class Meta:
        model = Basket_Item_dream
        fields = ['basket_dream', 'basket_heart', 'goods_id', 'buy_num', 'total_price', 'complete']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['basket_dream'].required = False
        self.fields['basket_heart'].required = False