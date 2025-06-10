from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category, Brand, Fighter

from .serializers import CategorySerializer, BrandSerializer, FighterSerializer, ProductSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from rest_framework.decorators import action


def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)
    fighters = Fighter.objects.filter(is_active=True)

    # Search functionality (case-insensitive)
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(sku__icontains=search_query)
        )

    # Filtering
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category__id=category_filter)

    brand_filter = request.GET.get('brand')
    if brand_filter:
        products = products.filter(brand__id=brand_filter)

    fighter_filter = request.GET.get('fighter')
    if fighter_filter:
        products = products.filter(fighters__id=fighter_filter)

    # Special filters
    if request.GET.get('featured'):
        products = products.filter(is_featured=True)
    if request.GET.get('bestseller'):
        products = products.filter(is_bestseller=True)
    if request.GET.get('new'):
        products = products.filter(is_new=True)

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'fighters': fighters,
        'search_query': search_query,
        'selected_category': int(category_filter) if category_filter else None,
        'selected_brand': int(brand_filter) if brand_filter else None,
        'selected_fighter': int(fighter_filter) if fighter_filter else None,
        'is_featured': bool(request.GET.get('featured')),
        'is_bestseller': bool(request.GET.get('bestseller')),
        'is_new': bool(request.GET.get('new')),
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(pk=pk)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class FighterViewSet(viewsets.ModelViewSet):
    queryset = Fighter.objects.all()
    serializer_class = FighterSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('images', 'sizes', 'fighters')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductFilter

    # Поиск по названию или краткому описанию
    search_fields = ['name', 'short_description']

    @action(methods=['GET'], detail=False)
    def new_products(self, request):
        """Вернуть список новинок"""
        new_items = self.queryset.filter(is_new=True)
        page = self.paginate_queryset(new_items)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(new_items, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=True)
    def mark_featured(self, request, pk=None):
        """Пометить товар как рекомендуемый"""
        product = self.get_object()
        product.is_featured = True
        product.save()
        return Response({'status': f'Товар {product.name} отмечен как рекомендуемый'})
