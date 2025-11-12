from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer, UserRegisterSerializer

from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework import viewsets
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.response import Response

# --- Custom Permission ---
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS for everyone
        if request.method in SAFE_METHODS:
            return True
        # Only admin users can modify data
        return request.user and request.user.is_staff

# --- Product ViewSet ---
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.all()
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        metal = self.request.query_params.get('metal')
        sort = self.request.query_params.get('sort')

        if min_price and max_price:
            queryset = queryset.filter(price__range=(min_price, max_price))
        if metal:
            queryset = queryset.filter(base_metal__icontains=metal)
        if sort == 'price_low':
            queryset = queryset.order_by('price')
        elif sort == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort == 'latest':
            queryset = queryset.order_by('-id')
        elif sort == 'popularity':
            queryset = queryset.order_by('-rating')

        return queryset


# --- Category ViewSet ---
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@api_view(['GET'])
def products_by_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=404)
    products = category.products.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


# --- User Registration ---
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
