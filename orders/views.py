from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from products.models import CartItem
from users.views import TitleMixin
from .forms import OrderForm
from .models import Order


class CreateOrderView(TitleMixin, CreateView):
    title = 'Checkout'
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:create_order')

    def get(self, request, *args, **kwargs):
        self.object = None
        fields = ('first_name', 'last_name', 'email')
        context = {field: getattr(self.request.user, field) for field in fields}
        context_data = self.get_context_data()
        context_data.update({'form': self.form_class(initial=context)})
        return self.render_to_response(context_data)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

