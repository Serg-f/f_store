from django.urls import path

from users.views import (EmailVerificationView, ProfileView, RegisterView,
                         UserLoginView, UserLogoutView, check_authentication_status)

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('verify/<int:pk>/<uuid:uuid>/', EmailVerificationView.as_view(), name='verify'),
    path('api/check_authentication/', check_authentication_status, name='check_authentication_status'),
]
