from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView, TemplateView
from django.http import JsonResponse

from .models import CartItem, ProdCategory, Product


class IndexView(TemplateView):
    template_name = 'products/index.html'
    extra_context = {'title': 'Store'}


class ProductsView(ListView):
    template_name = 'products/products.html'
    paginate_by = 6

    def get_queryset(self):
        self.cat_selected = get_object_or_404(ProdCategory, **self.kwargs) if self.kwargs.get('pk') else None
        return self.cat_selected.product_set.all() if self.cat_selected else Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None)
        context['title'] = self.cat_selected.name if self.cat_selected else 'Store - Catalog'
        context['cats'] = ProdCategory.objects.all()
        context.update(self.kwargs)
        return context


@login_required
def update_cart(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        cart_item_id = request.POST.get('cart_item_id')
        kwargs = {'id': cart_item_id, 'user': request.user}
        if not CartItem.objects.filter(**kwargs).exists():
            return JsonResponse({'status': 'error'})
        cart_item = CartItem.objects.get(**kwargs)

        if action == 'add':
            cart_item.quantity += 1
        elif action == 'minus':
            cart_item.quantity -= 1
            if cart_item.quantity == 0:
                cart_item.delete()
                return JsonResponse({'status': 'success', 'action': 'minus'})
        elif action == 'remove':
            cart_item.delete()
            return JsonResponse({'status': 'success', 'action': 'remove'})

        cart_item.save()
        return JsonResponse({
            'status': 'success',
            'action': action,
        })
    return JsonResponse({'status': 'error'})


@login_required
def add_cart_item(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        kwargs = {'product_id': product_id, 'user': request.user}
        if CartItem.objects.filter(**kwargs).exists():
            item = CartItem.objects.get(**kwargs)
            item.quantity += 1
            item.save()
        else:
            CartItem.objects.create(**kwargs, quantity=1)
        return JsonResponse({
            'status': 'success',
            'action': request.POST.get('action')
        })
    else:
        return JsonResponse({'status': 'error'})
