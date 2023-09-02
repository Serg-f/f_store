from django.contrib import admin
from django.utils.safestring import mark_safe

from products.models import CartItem, ProdCategory, Product

admin.site.register(ProdCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_html_photo', 'price', 'quantity')
    list_filter = ('category', 'price', 'quantity')
    search_fields = ('name',)
    readonly_fields = ('get_html_photo_edit',)
    fields = ('name', 'description', 'image', 'get_html_photo_edit', 'price', 'quantity', 'category')

    def get_html_photo(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width=50")

    def get_html_photo_edit(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width=200")

    get_html_photo.short_description = 'Photo'
    get_html_photo_edit.short_description = 'Photo preview'


class CartAdmin(admin.TabularInline):
    model = CartItem
    fields = ('product', 'quantity', 'create')
    readonly_fields = ('create',)
    extra = 0
