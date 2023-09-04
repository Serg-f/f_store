from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'create', 'status')
    readonly_fields = ('id', 'create')
    fields = ('id', 'create', ('first_name', 'last_name'), ('email', 'address'), 'cart_history', ('status', 'user'))
