from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import *

# Create your views here.

class CheckAPIView(APIView):
    def get(self, request, format=None):
        orders = Order.objects.filter(is_active=True)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    def post(self,request, format=None):
        serializer = OrderSerializer(data=request.data) 
        if serializer.is_valid():
            total_price = sum(item.get('nmb') * item.get('product').price for item in serializer.validated_data['items'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response
