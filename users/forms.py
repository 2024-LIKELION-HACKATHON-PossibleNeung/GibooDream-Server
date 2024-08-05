from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser, BeneficiaryApplication

#회원가입 폼
class SignUpForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('individual', 'Individual'),
        ('company', 'Company'),
        ('foreigner', 'Foreigner'),
    )
    email = forms.EmailField(required=True)
    nickname = forms.CharField(max_length=30, required=True)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect, required=True)
    terms1 = forms.BooleanField(required=True)
    terms2 = forms.BooleanField(required=True)
    terms3 = forms.BooleanField(required=True)
    terms4 = forms.BooleanField(required=False)
    terms5 = forms.BooleanField(required=False)

    class Meta:
        model = MyUser
        fields = ('email', 'nickname', 'user_type', 'password1', 'password2', 'terms1', 'terms2', 'terms3', 'terms4', 'terms5')
    
    def clean_terms1(self):
        terms1 = self.cleaned_data.get('terms1')
        if not terms1:
            raise forms.ValidationError("You must agree to terms 1")
        return terms1
    
    def clean_terms2(self):
        terms2 = self.cleaned_data.get('terms2')
        if not terms2:
            raise forms.ValidationError("You must agree to terms 2")
        return terms2
    
    def clean_terms3(self):
        terms3 = self.cleaned_data.get('terms3')
        if not terms3:
            raise forms.ValidationError("You must agree to terms 3")
        return terms3
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data

#수혜자 신청 폼
class BeneficiaryApplicationForm(forms.ModelForm):
    class Meta:
        model = BeneficiaryApplication
        fields = ['full_name', 'address', 'detailed_address', 'contact_number', 'id_number', 'proof_document', 'consent']

    def clean_consent(self):
        consent = self.cleaned_data.get('consent')
        if not consent:
            raise forms.ValidationError("You must agree to the collection and use of personal information")
        return consent

    def clean(self):
        cleaned_data = super().clean()
        detailed_address = cleaned_data.get("detailed_address")
    
    # detailed_address는 필수가 아니기에 추가 검증 필요 X
        return cleaned_data