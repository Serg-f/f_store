from django.contrib import admin

from products.admin import CartAdmin
from users.models import EmailVerification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    inlines = (CartAdmin,)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    fields = ('code', 'user', 'create', 'expiration',)
    readonly_fields = ('create', 'expiration',)
