from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, BrandViewSet, FighterViewSet, ProductViewSet

app_name = 'catalog'

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('brands', BrandViewSet)
router.register('fighters', FighterViewSet)
router.register('products', ProductViewSet)

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('api/', include(router.urls)),
]