from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, smart_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import send_normal_email
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class UserProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_image']

    def update(self, instance, validated_data):
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.save()
        return instance
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name', 'profile_image', 'email', 'date_joined']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    
    class Meta:
        model= User
        fields=[
            'email',
            'first_name',
            'last_name',
            'password',
        ]

    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password')
        )
        return user
    

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=5)
    password = serializers.CharField(max_length=68, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    first_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model=User
        fields=[
            'email',
            'first_name',
            'full_name',
            'password',
            'profile_image',
            'access_token',
            'refresh_token'
        ]
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid Username or Password")
        if not user.is_verified:
            raise AuthenticationFailed("Email has not been verified")
        user_tokens  = user.tokens()
        return {
            'email':user.email,
            'first_name': user.first_name,
            'full_name': user.get_full_name,
            'profile_image': user.profile_image,
            'access_token': user_tokens.get('access'),
            'refresh_token': user_tokens.get('refresh'),
        }

class PasswordResetRequestSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)

    class Meta:
        fields=['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email):
            user=User.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            site_domain=get_current_site(request).domain
            relative_link = reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token':token})
            abslink=f"http://{site_domain}{relative_link}"
            email_body=f"Hi use the link below to reset your passowrd \n {abslink}"
            data={
                'email_body': email_body,
                'email_subject': "Reset your Password",
                'to_email':user.email
            }
            send_normal_email(data)

        return super().validate(attrs)
    

class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password=serializers.CharField(max_length=100, min_length=6, write_only=True)
    uidb64=serializers.CharField(write_only=True)
    token=serializers.CharField(write_only=True)

    class Meta:
        fields= ["password",'confirm_password', 'uidb64', "token"]

    def validate(self, attrs):
        try:
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')
            password=attrs.get('password')
            confirm_password=attrs.get('confirm_password')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("reset link is invalid or has expired", 401)
            if password != confirm_password:
                raise AuthenticationFailed("password do not match")
            user.set_password(password)
            user.save()
        except Exception as e:
            return AuthenticationFailed("link is invalid")

        return super().validate(attrs)
      

class LogoutSerializer(serializers.Serializer):
    refresh_token=serializers.CharField()
    default_error_messages={
        'bad_token': ('Token is Invalid or Expired')
    }

    def validate(self, attrs):
        self.token=attrs.get('refresh_token')
        return attrs
    
    def save(self, **kwargs):
        try:
            token=RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')
