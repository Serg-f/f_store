from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.html import format_html
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import ContextMixin, TemplateView

from products.models import CartItem
from users.forms import UserLoginForm, UserProfileForm, UserRegisterForm
from users.models import EmailVerification, User


class TitleMixin(ContextMixin):
    title = 'Title'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs, title=self.title)


class UserLoginView(SuccessMessageMixin, TitleMixin, LoginView):
    title = 'Authorization'
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get_success_message(self, cleaned_data):
        return format_html(
            'Welcome, {username}! You have successfully logged in.',
            username=cleaned_data.get('username')
        )

    def get(self, request, *args, **kwargs):
        # Store the referrer URL in the session if it's not the login page itself
        referrer = request.META.get('HTTP_REFERER')
        if referrer and not referrer.endswith(reverse('users:login')) and \
                not referrer.endswith(reverse('users:register')) and \
                r'/users/verify/' not in referrer:
            request.session['referrer_url_before_login'] = referrer
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        # Get the value of 'next' from POST data
        next_url = self.request.POST.get('next')
        # If 'next' is provided and is not empty, use it as the redirect URL
        if next_url:
            return next_url
        # If there's a stored referrer URL in the session, use it
        if 'referrer_url_before_login' in self.request.session:
            referrer_url = self.request.session.pop('referrer_url_before_login')
            return referrer_url
        # Otherwise, use the default success URL (e.g., user's profile or homepage)
        return super().get_success_url()


class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        # Save the current URL to redirect back to it after logout
        self.next_page = request.META.get('HTTP_REFERER', '/')

        success_message = format_html(f'Goodbye, {request.user.username}! You have successfully logged out.')
        messages.success(request, success_message)

        return super().dispatch(request, *args, **kwargs)

    def get_next_page(self):
        """
        Return the URL to redirect to after processing this request.
        """
        return self.next_page or super().get_next_page()

class RegisterView(SuccessMessageMixin, TitleMixin, CreateView):
    title = 'Create an account'
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def get_success_message(self, cleaned_data):
        return format_html(
            'Your account has been successfully created. <br>'
            'To complete registration check your email and follow the link inside. <br>'
            'If you do not see the email - check the spam folder.'
        )


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, TitleMixin, UpdateView):
    title = 'Personal account'
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    success_message = 'Your profile data has been successfully changed!'

    def get_object(self, queryset=None):
        return self.request.user


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'Store - email verification'
    extra_context = {
        'header': 'Congratulations',
        'content': 'Your account has been successfully verified!',
    }

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get('pk'))
        email_verify_queryset = EmailVerification.objects.filter(user=user, code=kwargs.get('uuid'))
        if email_verify_queryset.exists():
            email_verify_obj = email_verify_queryset.last()
            if email_verify_obj.is_expired:
                email_verify_obj = EmailVerification.objects.create(user=user)
                email_verify_obj.send_verification_email()
                self.extra_context = {
                    'header': 'This link is expired',
                    'content': 'We have sent you a new one, check your email.',
                }
            else:
                user.is_verified_email = True
                user.save()
            return super().get(request, *args, **kwargs)
        else:
            return redirect('index')


def check_authentication_status(request):
    return JsonResponse({
        'is_authenticated': request.user.is_authenticated
    })