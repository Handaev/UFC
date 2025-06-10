import django_filters
from django.db.models import Q
from .models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    brand = django_filters.CharFilter(field_name='brand__name', lookup_expr='icontains')
    is_active = django_filters.BooleanFilter(field_name='is_active')
    is_bestseller = django_filters.BooleanFilter(field_name='is_bestseller')

    class Meta:
        model = Product
        fields = ['category', 'brand', 'is_active', 'is_bestseller']
