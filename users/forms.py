from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from users.models import User
from django import forms


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4",
        'placeholder': "Input user name",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4",
        'placeholder': "Input password",
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegisterForm(UserCreationForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input your name',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input your surname',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input your username',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input your email',
    }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input your password',
    }))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Confirm your password',
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    GENDERS = [
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'I am an alien'),
    ]

    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input',
        'size': '50',
    }), label='Choose an image', required=False)

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'aria-describedby': "usernameHelp",
        'readonly': True,
    }), label='User name')

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4',
        'aria-describedby': "emailHelp",
        'readonly': True,
    }), label='Email address')

    gender = forms.ChoiceField(choices=GENDERS, widget=forms.RadioSelect(attrs={
        'class': 'form-gender',
    }), label='Gender')

    birthday = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control',
        'placeholder': 'YYYY-MM-DD',
    }), label='Birthday')
    class Meta:
        model = User
        fields = ('image', 'first_name', 'last_name', 'username', 'email', 'gender', 'birthday',)
