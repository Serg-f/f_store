from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Product, ProdCategory, CartItem


def index(request):
    context = {'title': 'Store'}
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'Store - Catalog',
        'products': Product.objects.all(),
        'cats': ProdCategory.objects.all(),
    }
    return render(request, 'products/products.html', context)


@login_required
def cart_add(request, product_id):
    cart_item = CartItem.objects.get_or_create(user=request.user, product_id=product_id)[0]
    cart_item.quantity += 1
    cart_item.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def cart_remove(request, cart_item_id):
    CartItem(id=cart_item_id).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
