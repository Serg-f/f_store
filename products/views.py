from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView
from django.http import JsonResponse

from f_store.settings import PAGINATE_BY
from .models import CartItem, ProdCategory, Product


class IndexView(TemplateView):
    template_name = 'products/index.html'
    extra_context = {'title': 'F-Store'}


class ProductsView(ListView):
    template_name = 'products/products.html'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        self.cat_selected = get_object_or_404(ProdCategory, **self.kwargs) if self.kwargs.get('pk') else None
        return self.cat_selected.product_set.all() if self.cat_selected else Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None)
        context['title'] = self.cat_selected.name if self.cat_selected else 'F-Store - Catalog'
        context['cats'] = ProdCategory.objects.all()
        context.update(self.kwargs)
        return context


class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'
    model = Product
    context_object_name = 'prod'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_ids = tuple(self.object.category.product_set.values_list('id', flat=True))
        context['page_number'] = product_ids.index(self.object.id) // PAGINATE_BY + 1
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
            item = CartItem.objects.create(**kwargs, quantity=1)
        return JsonResponse({
            'status': 'success',
            'cartItemId': item.id,
        })
    else:
        return JsonResponse({'status': 'error'})
