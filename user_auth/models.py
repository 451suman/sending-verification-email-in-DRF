from django.contrib.auth.models import AbstractUser
from django.db import models
import pyotp
from django.utils import timezone
from rest_framework.views import APIView

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=6, null=True, blank=True)
    otp_generated_at = models.DateTimeField(null=True, blank=True)
    otp_secret = models.CharField(max_length=32, null=True, blank=True)

    def generate_email_otp(self):
        """Generate an OTP and set expiration time."""
        totp = pyotp.TOTP(self.otp_secret, interval=300)  # 5 mins validity
        return totp.now()

    def set_email_otp(self):
        """Save OTP and timestamp."""
        if not self.otp_secret:
            self.otp_secret = pyotp.random_base32()
            self.save()

        otp = self.generate_email_otp()
        self.email_otp = otp
        self.otp_generated_at = timezone.now()
        self.save()

    def verify_email_otp(self, otp):
        """Verify if the OTP matches and is not expired."""

        if self.email_otp == otp and timezone.now() - self.otp_generated_at <= timezone.timedelta(minutes=5):
            return True
        return False


