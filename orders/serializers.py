from rest_framework import serializers
from orders.models import Order, ProductInOrder

class ProductInOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ProductInOrder
        fields = (
            "product",
            "nmb",
        )
        
class OrderSerializer(serializers.ModelSerializer):
    items = ProductInOrderSerializer(many=True)
    class Meta:
        model = Order
        fields = (
            "id",
            "name",
            "phone",
            "address",
            'items',
        )
        
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            ProductInOrder.objects.create(order=order, **item_data)
        
        return order
        
class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInOrder
        fields = '__all__'  
