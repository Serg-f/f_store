import stripe
import logging
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView, ListView, DetailView, RedirectView
from http import HTTPStatus
from products.models import CartItem
from users.views import TitleMixin
from .forms import OrderForm
from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)


class SuccessView(TitleMixin, TemplateView):
    title = 'Thank you for the order!'
    template_name = 'orders/success.html'


class CancelView(LoginRequiredMixin, RedirectView):
    pattern_name = 'orders:create_order'

    def get(self, request, *args, **kwargs):
        order = request.user.order_set.last()
        if order.get_status_display() == 'Created':
            order.delete()
        return super().get(request, *args, **kwargs)


class CreateOrderView(LoginRequiredMixin, TitleMixin, CreateView):
    title = 'Checkout'
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:create_order')
    login_required()

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            if not request.user.cartitem_set.exists():
                form.add_error(None, "Cart is empty. Nothing to checkout.")
                return self.form_invalid(form)
            self.form_valid(form)
            # stripe checkout
            checkout_session = stripe.checkout.Session.create(
                line_items=request.user.cartitem_set.get_line_items(),
                metadata={'order_id': self.object.id},
                mode='payment',
                success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:success_order')),
                cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:cancel_order')),
            )
            return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        self.object = None
        fields = ('first_name', 'last_name', 'email', 'address')
        context = {field: getattr(self.request.user, field) for field in fields}
        context_data = self.get_context_data()
        context_data.update({'form': self.form_class(initial=context)})
        return self.render_to_response(context_data)

    def form_valid(self, form):
        user = form.instance.user = self.request.user
        fields = ('first_name', 'last_name', 'address')
        for field in fields:
            setattr(user, field, form.cleaned_data[field])
        user.save()
        return super().form_valid(form)


class OrdersListView(LoginRequiredMixin, TitleMixin, ListView):
    title = 'Orders'
    template_name = 'orders/orders.html'
    ordering = ('-id',)

    def get_queryset(self):
        return self.request.user.order_set.order_by(*self.ordering)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs, **{'title': f'Order №{self.object.id}'})


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        logger.error("Invalid payload: %s", e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:

        logger.error("Invalid signature: %s", e)
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items']
        )

        # Fulfill the purchase...
        fulfill_order(session.metadata)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(metadata):
    Order.objects.get(id=int(metadata.order_id)).update_after_payment()
