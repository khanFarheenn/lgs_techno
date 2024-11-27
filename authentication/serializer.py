from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from .models import *



temp_token_store = {}

        

# *******************************Register Serializer***********************************

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","email", "password", "first_name", "last_name"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            email=validated_data["email"],
            password=validated_data["password"],
        )

        # Set default role
        role, _ = Role.objects.get_or_create(name="REQUESTOR")
        user.role = role
        user.save()

        return user  
    
# {
#     "username": "farrheen1995",
#     "first_name": "farheen",
#     "last_name": "khan",
#     "email": "farrheenkhan1995@gmail.com",
#     "password": "farheen1995"
# }
    


# ***********************Login Serializer**************************

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not email and not username:
            raise serializers.ValidationError('Email or Username is required.')

        user = None
        if email:
            user = User.objects.filter(email=email).first()
        if username:
            user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            data['user'] = user
        else:
            raise serializers.ValidationError('Invalid username/email or password.')

        return data

#********************** MyCustomTokenSerializer***********************
class MyCustomTokenSerializer(serializers.Serializer):
    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        if user.role:
            token["role"] = user.role.name
        else:
            token["role"] = "No Role"  
        return token

# *************************Logout Serializer****************************
class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
    
    
    

# ***********************Change Password Serializer**********
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        user.set_password(validated_data['new_password'])
        user.save()
        return user

# ********************Forgot Password Serializer*************************

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
       
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email not found.')
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        
        reset_token = get_random_string(length=32)
        print(f"Generated Reset Token: {reset_token}")
        
       
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

        
        temp_token_store[reset_token] = email

     
        send_mail(
            subject='Password Reset Request',
            
            message=(
                    f'Use this link to reset your password: {reset_link}\n'
                    f'Your reset token is: {reset_token}'  
                ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
            # html_message=(
            #         f'Use this link to reset your password: <a href="{reset_link}">Reset Password</a><br>'
            #         f'Your reset token is: <strong>{reset_token}</strong>' 
            #     ),
             html_message=f'Use this link to reset your password: <a href="{reset_link}">Reset Password</a>'
        )
        print(f"Password reset link: {reset_link}")
        
        
        
# *************************Reset Password Serializer*************************

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate_token(self, value):
        if value not in temp_token_store:
            raise serializers.ValidationError('Invalid or expired token.')
        return value
