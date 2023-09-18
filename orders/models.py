from django.db import models
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

