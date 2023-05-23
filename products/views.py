from django.shortcuts import render
from .models import Products, ProdCategory


def index(request):
    context = {'title': 'Store'}
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'Store - Catalog',
        'products': Products.objects.all(),
        'cats': ProdCategory.objects.all(),
    }
    return render(request, 'products/products.html', context)
