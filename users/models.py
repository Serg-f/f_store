import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from f_store.settings import DOMAIN_NAME, EMAIL_HOST_USER


class User(AbstractUser):
    GENDERS = [
        ('m', 'Male'),
        ('f', 'Female'),
    ]
    image = models.ImageField(upload_to='users_image', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDERS, default='m')
    birthday = models.DateField(blank=True, null=True, default=None)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=256, blank=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True)

    @property
    def expiration(self):
        return self.create + timedelta(hours=48)

    @property
    def is_expired(self):
        return now() >= self.expiration

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        subject = f'F-Store: account verification for {self.user.username}'
        link = DOMAIN_NAME + reverse('users:verify', kwargs={'pk': self.user_id, 'uuid': self.code})
        message = f'To complete account registration for "{self.user.email}" follow the link: \n{link}'
        send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )
