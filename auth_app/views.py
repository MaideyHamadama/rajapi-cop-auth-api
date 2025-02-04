from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenVerifyView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import check_password
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from .serializers import *
from .models import *

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            raise ValidationError({'email' : "This field is required"})
        
        try:
            user = CustomUser.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            
            reset_url = f"http://127.0.0.1:8000/auth/reset-password/{uidb64}/{token}"
            
            send_mail(
                'Password Reset Request',
                f"Click the link to reset your password: {reset_url}",
                'noreply@rajapi-cop.com',
                [user.email]
            )
            return Response({"detail" : "Password reset email sent"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"detail" : "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, uidb64, token):
        try:
            # Decode the user ID
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (CustomUser.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({"detail": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)
        
        token_generator = PasswordResetTokenGenerator()
        
        # Validate the token
        if not token_generator.check_token(user, token):
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the new password from the request data
        new_password = request.data.get("new_password")
        confirm_password = request.data.get('confirm_password')
        if not new_password or not confirm_password:
            return Response({"detail": "Both password and confirm_password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if new_password != confirm_password:
            return Response({"detail": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
        # Reset the password
        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
    
def LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail' : 'Logged out successfully.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail" : "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Custom Token Verify view
class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(request.data)
        token = request.data.get('token', None)
        
        if not token:
            return Response({"token_valid": False, "detail": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Decode the token
            decoded_token = AccessToken(token)
            user_id = decoded_token['user_id']
            user = CustomUser.objects.get(id=user_id)
            user = CustomUser.objects.get(id=user_id)
            user_profile = UserProfileSerializer(user).data
            
            return Response({
                'token_valid' : True,
                'user_profile' : user_profile
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'token_valid':False,
                'detail':str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)
            
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not check_password(serializer.validated_data['old_password'], user.password):
                return Response({"error" : "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message" : "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeactivateAccountView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({"message" : "Account deactivated successfully."}, status=status.HTTP_200_OK)
    