from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class UserRegistrationTestCase(TestCase):
    def setUp(self) -> None:
        self.path = reverse('users:register')
        self.data = {
            'first_name': 'James',
            'last_name': 'Bond',
            'username': 'jamesbond',
            'email': 'bond@mail.com',
            'password1': 'MartiniVodka007',
            'password2': 'MartiniVodka007'
        }

    def test_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Create an account')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_post_success(self):
        username = self.data['username']
        # user creation
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)
        self.assertTrue(User.objects.filter(username=self.data['username']).exists())
        self.assertRedirects(response, reverse('users:login'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        # email verification
        email_verification_qs = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification_qs.exists())
        self.assertEqual(email_verification_qs.last().expiration.date(), (now() + timedelta(hours=48)).date())

    def test_post_user_exists_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'A user with that username already exists.',)
