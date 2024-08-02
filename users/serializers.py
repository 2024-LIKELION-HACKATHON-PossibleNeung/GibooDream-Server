from .models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = MyUser.objects.create_user(
            email = validated_data['email'],
            nickname = validated_data['nickname'],
            user_type = validated_data['user_type'],
            password = validated_data['password'],
            terms1=validated_data['terms1'],
            terms2=validated_data['terms2'],
            terms3=validated_data['terms3'],
            terms4=validated_data.get('terms4', False),
            terms5=validated_data.get('terms5', False),
        )
        return user
    def validate(self, data):
        if not data.get('terms1', False):
            raise serializers.ValidationError("Terms 1 must be accepted")
        if not data.get('terms2', False):
            raise serializers.ValidationError("Terms 2 must be accepted")
        if not data.get('terms3', False):
            raise serializers.ValidationError("Terms 3 must be accepted")
        return data
    
    class Meta:
        model = MyUser
        fields = ['nickname', 'email', 'user_type', 'password', 'terms1', 'terms2', 'terms3', 'terms4', 'terms5']
