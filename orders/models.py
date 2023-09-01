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
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=CREATED)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
