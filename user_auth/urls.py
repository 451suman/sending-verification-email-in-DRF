from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterUserViewSet, VerifyEmailOTPView

router = DefaultRouter()
router.register(r'register', RegisterUserViewSet, basename='register')

urlpatterns = [
    path('api/', include(router.urls)),
    path('verify-email-otp/', VerifyEmailOTPView.as_view(), name='verify-email-otp'),
]
