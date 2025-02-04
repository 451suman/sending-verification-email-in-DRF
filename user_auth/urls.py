from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterUserViewSet, VerifyEmailOTPView
from user_auth import views

router = DefaultRouter()
router.register(r'register', RegisterUserViewSet, basename='register')

urlpatterns = [
    path('api/', include(router.urls)),
    path('verify-email-otp/', VerifyEmailOTPView.as_view(), name='verify-email-otp'),
    path("login/", views.LoginViewSet.as_view(), name= "login"),
]
