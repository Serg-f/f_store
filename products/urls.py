from django.urls import path

from products.views import ProductsView, update_cart, add_cart_item, ProductDetailView

app_name = 'products'

urlpatterns = [
    path('category/<int:pk>', ProductsView.as_view(), name='category'),
    path('cart/update/', update_cart, name='update_cart'),
    path('cart/add-item/', add_cart_item, name='add_cart_item'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='detail'),
]
