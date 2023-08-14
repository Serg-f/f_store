from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, TemplateView

from .models import CartItem, ProdCategory, Product


class IndexView(TemplateView):
    template_name = 'products/index.html'
    extra_context = {'title': 'Store'}


class ProductsView(ListView):
    template_name = 'products/products.html'
    paginate_by = 3

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
def cart_add(request, product_id):
    cart_item = CartItem.objects.get_or_create(user=request.user, product_id=product_id)[0]
    cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f'{cart_item.product.name} added to cart.')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def cart_remove(request, cart_item_id):
    CartItem(id=cart_item_id).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
