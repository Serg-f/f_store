from django.urls import path

from products.views import ProductsView, ProductDetailView, \
    AddCartItemView, UpdateCartItemView, GetCartView, SetCartView

app_name = 'products'

urlpatterns = [
    path('category/<int:pk>', ProductsView.as_view(), name='category'),
    path('cart/update/', UpdateCartItemView.as_view(), name='update_cart'),
    path('cart/add-item/', AddCartItemView.as_view(), name='add_cart_item'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('cart-items/', GetCartView.as_view(), name='get_cart_items'),
    path('cart/save/', SetCartView.as_view(), name='save_cart'),
]
