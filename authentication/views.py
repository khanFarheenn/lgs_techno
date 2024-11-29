from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import *


class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'detail': 'User created successfully.'})
        return Response(serializer.errors)

# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             refresh = RefreshToken.for_user(user)
#             access_token = str(refresh.access_token)
#             refresh_token = str(refresh)
#             return Response({
#                 'access': access_token,
#                 'refresh': refresh_token,
#                 'role': user.role.name if user.role else "No Role"
#             }, status=status.HTTP_200_OK)
#         return Response(serializer.errors)

import logging
from django.contrib.auth.signals import user_logged_in
# Create a logger to capture actions
logger = logging.getLogger(__name__)

class LoginView(APIView):
    def post(self, request):
        # Deserialize the incoming data with LoginSerializer
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Manually trigger the user_logged_in signal after successful login
            logger.info(f"Manually triggering the user_logged_in signal for user {user.email}.")
            user_logged_in.send(sender=user.__class__, request=request, user=user)
            
            # Generate the JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # Return the response with the tokens and user role
            return Response({
                'access': access_token,
                'refresh': refresh_token,
                'role': user.role.name if user.role else "No Role"
            }, status=status.HTTP_200_OK)
        
        # If validation fails, return errors
        return Response(serializer.errors)


class LogoutView(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            refresh_token = serializer.validated_data['refresh_token']
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'detail': 'Logged out successfully.'})
            except Exception as e:
                return Response({'detail': 'Invalid token.'})
        return Response(serializer.errors)

class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Password changed successfully.'})
        return Response(serializer.errors)

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Password reset email sent.'})
        return Response(serializer.errors)

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            reset_token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']

            # Reset password
            email = temp_token_store.get(reset_token)
            if email:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()

                # Remove the token from temp store
                del temp_token_store[reset_token]

                return Response({'detail': 'Password reset successful.'})
            return Response({'detail': 'Invalid or expired token.'})
        return Response(serializer.errors)



