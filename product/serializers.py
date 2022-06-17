from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken,TokenError 



class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'   
        

class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, min_length=3)
    email = serializers.EmailField(max_length=50, min_length=3)
    password = serializers.CharField(max_length=150, write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email','password')
        
    def validate(self, args):
        username = args.get('username', None)
        email = args.get('email', None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ('email already exists')})
        else:
            pass
        return super().validate(args)
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': {'Token is expired or invalid'}
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
            
        except TokenError:
            self.fail('bad_token')
            

class ContactSerializer(serializers.Serializer):
    
    class Meta:
        model = Contact
        fields = ('id', 'username', 'gmail','message')
    
    def create(self, validated_data):
        return Contact.objects.create()