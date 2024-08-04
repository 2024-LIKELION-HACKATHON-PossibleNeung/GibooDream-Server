# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from .models import BeneficiaryApplication

MyUser = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    terms1 = serializers.BooleanField(write_only=True)
    terms2 = serializers.BooleanField(write_only=True)
    terms3 = serializers.BooleanField(write_only=True)
    terms4 = serializers.BooleanField(required=False, write_only=True)
    terms5 = serializers.BooleanField(required=False, write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'nickname', 'user_type', 'password', 'terms1', 'terms2', 'terms3', 'terms4', 'terms5']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        terms_fields = ['terms1', 'terms2', 'terms3']
        for field in terms_fields:
            if not data.get(field):
                raise serializers.ValidationError({field: 'This field is required.'})
        return data

    def create(self, validated_data):
        validated_data.pop('terms1')
        validated_data.pop('terms2')
        validated_data.pop('terms3')
        validated_data.pop('terms4')
        validated_data.pop('terms5')
        user = MyUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError(_('Unable to log in with provided credentials.'))
        
        else:
            raise serializers.ValidationError(_('Must include "email" and "password".'))
    
        data['user'] = user
        return data

class BeneficiaryApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeneficiaryApplication
        fields = '__all__'
        read_only_fields = ['status', 'user']