from django.core.mail import send_mail
from django.db import models
from django.urls import reverse

from f_store.settings import DOMAIN_NAME, EMAIL_HOST_USER
from users.models import User


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_THE_WAY = 2
    DELIVERED = 3
    CANCELED = 4
    STATUSES = [
        (CREATED, 'Created'),
        (PAID, 'Paid'),
        (ON_THE_WAY, 'On the way'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
    ]
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    address = models.CharField(max_length=128)
    create = models.DateTimeField(auto_now_add=True)
    cart_history = models.JSONField(default=dict)
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=CREATED)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order #{self.id} for {self.first_name} {self.last_name}'

    def update_after_payment(self):
        items = self.user.cartitem_set.all()
        self.status = self.PAID
        self.cart_history = {
            'items': [item.get_dict() for item in items],
            'total_cost': str(items.total_cost()),
        }
        self.save()
        items.delete()

    def send_user_order_status_email(self):
        subject = f'F-Store. Updating your order №{self.id} status: {self.get_status_display()}'
        link = DOMAIN_NAME + reverse('orders:order_detail', kwargs={'pk': self.id})
        message = f'Hello {self.first_name} {self.last_name},\n' \
            f'Your order №{self.id} has received new status: {self.get_status_display()}\n' \
            f'Delivery address: {self.address}\n' \
            'To check order details follow the link:\n' \
            f'{link}'

        send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[self.email],
            fail_silently=False,
        )

        subject = f'F-Store. Order #{self.id} status: {self.get_status_display()}'
        link = DOMAIN_NAME + reverse('admin:orders_order_change', kwargs={'object_id': self.id})
        message = [f'Order #{self.id} status: {self.get_status_display()}',
                   f'Admin panel detail link: {link}',
                   f'First name, last name: {self.first_name} {self.last_name}',
                   f'Total cost: {self.cart_history["total_cost"]}',
                   f'Delivery address: {self.address}',
                   'Items:\n']
        for i, item in enumerate(self.cart_history['items'], start=1):
            message.append(f'    {i}.')
            message.append(f'    Id: {item["id"]}')
            message.append(f'    Name: {item["name"]}')
            message.append(f'    Quantity: {item["quantity"]}')
            message.append(f'    Price: {item["price"]}')
            message.append(f'    Cost: {item["cost"]}\n')

        send_mail(
            subject=subject,
            message='\n'.join(message),
            from_email=EMAIL_HOST_USER,
            recipient_list=[EMAIL_HOST_USER],
            fail_silently=False,
        )
