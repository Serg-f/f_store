from celery import shared_task
from .models import Order


@shared_task
def update_order_status(order_id, status):
    order = Order.objects.get(id=order_id)
    order.status = status
    order.save()
    order.send_user_order_status_email()
