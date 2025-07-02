from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
import uuid

from .models import Admin, AdminPassword
from .serializers import AdminSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({
            'success': False,
            'result': None,
            'message': 'Email and password are required',
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(email=email, password=password)
    
    if not user:
        return Response({
            'success': False,
            'result': None,
            'message': 'Invalid credentials',
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.enabled:
        return Response({
            'success': False,
            'result': None,
            'message': 'Your account is disabled',
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    if user.removed:
        return Response({
            'success': False,
            'result': None,
            'message': 'Your account has been removed',
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Generate token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    
    # Store token in logged sessions
    admin_password, created = AdminPassword.objects.get_or_create(user=user)
    if not created and not admin_password.logged_sessions:
        admin_password.logged_sessions = []
    
    admin_password.logged_sessions.append(access_token)
    admin_password.save()
    
    # Return user data and token
    serializer = AdminSerializer(user)
    
    return Response({
        'success': True,
        'result': {
            'token': access_token,
            'admin': serializer.data
        },
        'message': 'Login successful',
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def logout(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({
            'success': False,
            'result': None,
            'message': 'No authentication token provided',
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    token = auth_header.split(' ')[1]
    user = request.user
    
    try:
        admin_password = AdminPassword.objects.get(user=user)
        if token in admin_password.logged_sessions:
            admin_password.logged_sessions.remove(token)
            admin_password.save()
        
        return Response({
            'success': True,
            'result': None,
            'message': 'Logout successful',
        }, status=status.HTTP_200_OK)
    except AdminPassword.DoesNotExist:
        return Response({
            'success': False,
            'result': None,
            'message': 'User password record not found',
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def forget_password(request):
    email = request.data.get('email')
    
    if not email:
        return Response({
            'success': False,
            'result': None,
            'message': 'Email is required',
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = Admin.objects.get(email=email, removed=False)
        
        # Generate reset token
        reset_token = str(uuid.uuid4())
        expires = timezone.now() + timedelta(hours=1)
        
        # Store token
        admin_password, created = AdminPassword.objects.get_or_create(user=user)
        admin_password.password_reset_token = reset_token
        admin_password.password_reset_expires = expires
        admin_password.save()
        
        # In a real application, send an email with the reset link
        # For now, we'll just return the token in the response
        
        return Response({
            'success': True,
            'result': {
                'resetToken': reset_token,
                'email': email
            },
            'message': 'Password reset instructions sent to your email',
        }, status=status.HTTP_200_OK)
    except Admin.DoesNotExist:
        return Response({
            'success': False,
            'result': None,
            'message': 'No user found with this email',
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    email = request.data.get('email')
    token = request.data.get('resetToken')
    password = request.data.get('password')
    
    if not email or not token or not password:
        return Response({
            'success': False,
            'result': None,
            'message': 'Email, reset token, and new password are required',
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = Admin.objects.get(email=email, removed=False)
        admin_password = AdminPassword.objects.get(user=user)
        
        # Verify token
        if admin_password.password_reset_token != token:
            return Response({
                'success': False,
                'result': None,
                'message': 'Invalid reset token',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if token is expired
        if admin_password.password_reset_expires < timezone.now():
            return Response({
                'success': False,
                'result': None,
                'message': 'Reset token has expired',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Reset password
        user.set_password(password)
        user.save()
        
        # Clear reset token
        admin_password.password_reset_token = None
        admin_password.password_reset_expires = None
        admin_password.save()
        
        return Response({
            'success': True,
            'result': None,
            'message': 'Password has been reset successfully',
        }, status=status.HTTP_200_OK)
    except Admin.DoesNotExist:
        return Response({
            'success': False,
            'result': None,
            'message': 'No user found with this email',
        }, status=status.HTTP_404_NOT_FOUND)
    except AdminPassword.DoesNotExist:
        return Response({
            'success': False,
            'result': None,
            'message': 'User password record not found',
        }, status=status.HTTP_404_NOT_FOUND)