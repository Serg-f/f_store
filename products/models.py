from django.db import models
from users.models import User
from django.conf import settings
from ckeditor.fields import RichTextField
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProdCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Product(models.Model):
    name = models.CharField(max_length=250)
    description = RichTextField()
    image = models.ImageField(upload_to='prod_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    stripe_price_id = models.CharField(max_length=128, blank=True)
    category = models.ForeignKey(to=ProdCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category} | {self.name}'

    def create_stripe_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_price = stripe.Price.create(
            unit_amount=int(self.price * 100),
            currency="eur",
            product=stripe_product.stripe_id,
        )
        return stripe_price

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_price_id:
            self.stripe_price_id = self.create_stripe_price().stripe_id
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    class Meta:
        ordering = ['image']


class CartQuerySet(models.QuerySet):
    def total_quantity(self):
        return sum(item.quantity for item in self)

    def total_cost(self):
        return sum(item.cost() for item in self)

    def get_line_items(self):
        line_items = []
        for cart_item in self:
            line_item = {
                'price': cart_item.product.stripe_price_id,
                'quantity': cart_item.quantity,
            }
            line_items.append(line_item)
        return line_items


class CartItem(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    create = models.DateTimeField(auto_now_add=True)

    objects = CartQuerySet.as_manager()

    def __str__(self):
        return f'{self.user.username} | {self.product}: {self.quantity}'

    def cost(self):
        return self.quantity * self.product.price

    def get_dict(self):
        return {
            'id': self.product.id,
            'name': self.product.name,
            'quantity': self.quantity,
            'price': str(self.product.price),
            'cost': str(self.cost())
        }
