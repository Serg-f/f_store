import json

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from f_store.settings import PAGINATE_BY
from .models import CartItem, ProdCategory, Product
from .serializers import CartProductSerializer, CartItemSerializer, GetCartSerializer, SetCartSerializer


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


class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            cart_item_id = serializer.validated_data['cart_item_id']
            action = serializer.validated_data['action']
            kwargs = {'id': cart_item_id, 'user': request.user}
            if not CartItem.objects.filter(**kwargs).exists():
                return Response({'status': 'error'})
            cart_item = CartItem.objects.get(**kwargs)

            if action == 'add':
                cart_item.quantity += 1
            elif action == 'minus':
                cart_item.quantity -= 1
                if cart_item.quantity == 0:
                    cart_item.delete()
                    return Response({'status': 'success'})
            elif action == 'remove':
                cart_item.delete()
                return Response({'status': 'success'})

            cart_item.save()
            return Response({
                'status': 'success',
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CartProductSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            kwargs = {'product_id': product_id, 'user': request.user}
            if CartItem.objects.filter(**kwargs).exists():
                item = CartItem.objects.get(**kwargs)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(**kwargs, quantity=1)

            return Response({
                'status': 'success',
                'cartItemId': item.id,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCartView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetCartSerializer

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return Response({
            'status': 'success',
            'cartItems': self.serializer_class(self.get_queryset(), many=True).data,
        })


def save_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        CartItem.objects.filter(user=request.user).delete()
        for item in data.values():
            CartItem.objects.create(user=request.user, product_id=item['productId'], quantity=item['quantity'])
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


class SetCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SetCartSerializer(data=request.data, many=True)
        if serializer.is_valid():
            CartItem.objects.filter(user=request.user).delete()
            CartItem.objects.bulk_create([
                CartItem(user=request.user, **item) for item in serializer.validated_data
            ])

            return Response({'status': 'success'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
