from rest_framework import serializers

from products.models import CartItem, Product


class CartProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()


class CartItemSerializer(serializers.Serializer):
    cart_item_id = serializers.IntegerField()
    action = serializers.CharField(max_length=10)


class GetCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id')
    name = serializers.CharField(source='product.name')
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)
    image = serializers.ImageField(source='product.image')

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'name', 'price', 'image', 'quantity']
        read_only_fields = ['id', 'product_id', 'name', 'price', 'image', 'quantity']


class SetCartSerializer(serializers.ModelSerializer):
    productId = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product')

    class Meta:
        model = CartItem
        fields = ['productId', 'quantity']
