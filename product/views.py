import math
from django.views.generic import ListView
from numpy import sort
from rest_framework.filters import OrderingFilter
from .pagination import ProductPagination
from .serializers import ProductListSerializer, RegistrationSerializer, LogoutSerializer, ContactSerializer
from product.models import Product, Contact
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
import uuid
from rest_framework.views import APIView
from rest_framework import filters, generics, status, permissions
from django.core.mail import send_mail
from django.db.models import Q



class HomePageView(ListView):
    model = Product
    context_object_name = 'product_list'
    queryset = Product.objects.filter(is_published=True).order_by('-updated_date')
    template_name = 'product/index.html'
    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView,self).get_context_data(*args, **kwargs)
        context["images"] = Product.objects.filter(is_published=True).order_by('-updated_date')
        return context
    

class ProductListView(APIView):
    # def get(self, request):
    #     s= request.GET.get('s')
    #     page = int(request.GET.get('page',1))
    #     per_page = 9
        
    #     products = Product.objects.filter(is_published=True).order_by('-updated_date')
    #     if s:
    #         products = products.filter(Q(category__id__icontains=s))
    #     total = products.count()
    #     start = (page-1)*per_page
    #     end = page * per_page
    #     serializer = ProductListSerializer(products[start:end], many=True)
    #     return Response({
    #         'data': serializer.data, 
    #         'total':total, 
    #         'page':page,
    #         'last_page': math.ceil(total/per_page)
    #         })
        
        
    queryset = Product.objects.filter(is_published=True).order_by('-updated_date')
    search_fields = ['title']
    serializer_class = ProductListSerializer
    pagination_class = ProductPagination
    filter_backends = [OrderingFilter, filters.SearchFilter]
    ordering_fields = ['category']

    def get_queryset(self):
        queryset = Product.objects.filter(is_published=True).order_by('-updated_date')
        p = self.request.query_params
        category = p.get('filter', None)
        if category == None or category == '0':
                queryset = queryset.filter()
        elif p:
            queryset = queryset.filter(category=category)
        return queryset
    
class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "RequestId": str(uuid.uuid4()),
                "Message": "User created successfully",
                "User": serializer.data}, status = status.HTTP_201_CREATED
                )
        return Response({"Errors": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)


class BlacklistTokenAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
       serializer = self.serializer_class(data=request.data)
       serializer.is_valid(raise_exception=True)
       serializer.save()
       
       return Response(status=status.HTTP_204_NO_CONTENT)

class SecretAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        return Response('Success') 
 
 
class ContactAPIView(APIView):
    def get(self, request, format=None):
        orders = Contact.objects.filter()
        serializer = ContactSerializer(orders, many=True)
        return Response(serializer.data)
    
    def post(self,request, format=None):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = request.data['username']
            gmail = request.data['gmail']
            message = request.data['message']
            send_mail(f'{username} от {gmail}', message,
                          gmail, ['webprogcoder@gmail.com'], fail_silently=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BrandListAPIView(ListAPIView):
    queryset = Product.objects.filter(is_published=True).order_by('-updated_date')
    serializer_class = ProductListSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['category']

    def get_queryset(self):
        queryset = Product.objects.filter(is_published=True).order_by('-updated_date')
        p = self.request.query_params
        category = p.get('filter', None)
        if p:
            queryset = queryset.filter(category=category)[:4]
        return queryset
    