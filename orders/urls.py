from django.urls import path
from orders.views import CreateOrderView, SuccessView, CancelView, OrdersListView, OrderDetailView
app_name = 'orders'

urlpatterns = [
    path('create-order/', CreateOrderView.as_view(), name='create_order'),
    path('success-order/', SuccessView.as_view(), name='success_order'),
    path('cancel-order/', CancelView.as_view(), name='cancel_order'),
    path('orders-list/', OrdersListView.as_view(), name='orders_list'),
    path('order-detail/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    
]
