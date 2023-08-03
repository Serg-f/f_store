from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import ContextMixin

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView

from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from products.models import CartItem
from users.models import User

from django.urls import reverse_lazy
from django.contrib import messages


class TitleMixin(ContextMixin):
    title = 'Title'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs, title=self.title)


class UserLoginView(SuccessMessageMixin, TitleMixin, LoginView):
    title = 'Authorization'
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_message = 'Welcome, %(username)s!\nYou have successfully logged in.'


class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, f'Good by, {request.user.username}!\nYou have successfully logged out.')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(SuccessMessageMixin, TitleMixin, CreateView):
    title = 'Create an account'
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'You have been successfully registered!'


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, TitleMixin, UpdateView):
    title = 'Personal account'
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    success_message = 'Your profile data has been successfully changed!'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_items'] = CartItem.objects.filter(user=self.object)
        return context
