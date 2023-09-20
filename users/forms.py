from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.core.exceptions import ValidationError

from users.models import EmailVerification, User


class SetHtmlClassMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        fields_for_edit = ('first_name', 'last_name', 'username', 'email', 'password', 'password1', 'password2')
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in fields_for_edit:
                field.widget.attrs['class'] = 'form-control py-4'


class UserLoginForm(SetHtmlClassMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "Input user name"
        self.fields['password'].widget.attrs['placeholder'] = "Input password"

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_verified_email:
            raise ValidationError("To login please confirm your email first")

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegisterForm(SetHtmlClassMixin, UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_placeholder = {
            'first_name': 'Input your name',
            'last_name': 'Input your surname',
            'username': 'Input your username',
            'email': 'Input your email',
            'password1': 'Input your password',
            'password2': 'Confirm your password'
        }
        for name, placeholder in set_placeholder.items():
            self.fields[name].widget.attrs['placeholder'] = placeholder

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=True)
        email_verification_object = EmailVerification.objects.create(user=user)
        email_verification_object.send_verification_email()
        return user


class UserProfileForm(SetHtmlClassMixin, UserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['username'].label = 'User name'
        self.fields['email'].disabled = True

    class Meta:
        model = User
        fields = ('image', 'first_name', 'last_name', 'username', 'email', 'gender', 'birthday', 'address')
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'custom-file-input',
                'size': '50',
            }),
            'gender': forms.RadioSelect(attrs={
                'class': "form-gender",
            }),
            'birthday': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
        }
