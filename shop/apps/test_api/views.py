from django.shortcuts import render
from apps.products.models import Product
from rest_framework.views import APIView 
from .Serializers import ProductSerializer
from rest_framework.response import Response
# Create your views here.

class AllProductsApi(APIView):
    def get(self, request):
        products = Product.objects.filter(is_active=True).order_by('-published_date')
        self.check_object_permissions(request, products)
        ser_data = ProductSerializer(instance=products, many=True)
        return Response(data=ser_data.data)