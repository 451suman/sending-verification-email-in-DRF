from rest_framework import status, viewsets
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import CustomUser  # Import the correct model
from .serializers import LoginSerializer, UserSerializer, EmailOTPVerifySerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class RegisterUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Override the create method to include OTP logic
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Save the user and generate OTP
            user = serializer.save()
            
            # Generate and save OTP to the user model
            user.set_email_otp()
            
            # Send OTP email
            send_mail(
                'Email Verification OTP',
                f'Your OTP for email verification is: {user.email_otp}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            
            return Response(
                {"message": "User created successfully. OTP sent to your email."},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class VerifyEmailOTPView(APIView):
    def post(self, request):
        serializer = EmailOTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email_otp = serializer.validated_data['email_otp']
            try:
                user = CustomUser.objects.get(email=request.data['email'])
            except CustomUser.DoesNotExist:
                return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            # Use Django's timezone.now() here
            if user.verify_email_otp(email_otp):
                user.is_email_verified = True
                user.email_otp = None  # Clear OTP after successful verification
                user.save()
                return Response({'detail': 'Email successfully verified'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from django.contrib.auth.hashers import check_password
# class LoginViewSet(APIView):
#     serializer_class = LoginSerializer

#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         try:
#             user = CustomUser.objects.get(username=username)
#         except CustomUser.DoesNotExist:
#             # Return specific error if username is incorrect
#             return Response({
#                 "status": "failed",
#                 "message": "Username is incorrect"
#             })
        
#         if not check_password(password, user.password):
#             # Return specific error if password is incorrect
#             return Response({
#                 "status": "failed",
#                 "message": "Password is incorrect"
#             })

       
    