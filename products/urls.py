from django.urls import path
from products.views import products, cart_add, cart_remove

app_name = 'products'

urlpatterns = [
    path('', products, name='index'),
    path('cart/add/<int:product_id>', cart_add, name='cart_add'),
    path('cart/remove/<int:cart_item_id>', cart_remove, name='cart_remove'),
]
