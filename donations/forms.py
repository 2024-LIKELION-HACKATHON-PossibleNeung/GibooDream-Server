from django import forms
from .models import *

class BasketItemDreamForm(forms.ModelForm):
    class Meta:
        model = Basket_Item_dream
        fields = ['basket_dream', 'basket_heart','buy_num', 'total_price', 'complete']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['basket_dream'].required = False
        self.fields['basket_heart'].required = False

class ReviewForm(forms.ModelForm):
    donation_id = forms.ModelChoiceField(queryset=CopyOfDonation.objects.all(), label='Donation ID')

    class Meta:
        model = Review
        fields = ['donation_id', 'review_cont', 'review_img']