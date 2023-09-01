from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .forms import OrderForm
from .models import Order


class CreateOrderView(CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    model = Order



