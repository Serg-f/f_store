from django.contrib import admin

from products.models import CartItem, ProdCategory, Product

admin.site.register(ProdCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')
    list_filter = ('category', 'price', 'quantity')
    search_fields = ('name',)


class CartAdmin(admin.TabularInline):
    model = CartItem
    fields = ('product', 'quantity', 'create')
    readonly_fields = ('create',)
    extra = 0

