from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from users.models import User
from django import forms


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


class UserProfileForm(SetHtmlClassMixin, UserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['username'].label = 'User name'
        self.fields['email'].disabled = True

    class Meta:
        model = User
        fields = ('image', 'first_name', 'last_name', 'username', 'email', 'gender', 'birthday',)
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
