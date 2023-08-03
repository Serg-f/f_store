from django.urls import path
from products.views import ProductsView, cart_add, cart_remove

app_name = 'products'

urlpatterns = [
    path('category/<int:pk>/', ProductsView.as_view(), name='category'),
    path('cart/add/<int:product_id>/', cart_add, name='cart_add'),
    path('cart/remove/<int:cart_item_id>/', cart_remove, name='cart_remove'),
]
