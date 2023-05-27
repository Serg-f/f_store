from django.urls import path
from users.views import login, register
app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', register, name='register'),

]