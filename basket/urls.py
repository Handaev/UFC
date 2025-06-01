from django.urls import path
from . import views

app_name = 'basket'

urlpatterns = [
    path('', views.basket_detail, name='detail'),
    path('add/<int:product_id>/', views.basket_add, name='add'),
    path('remove/<int:item_id>/', views.basket_remove, name='remove'),
    path('update/<int:item_id>/', views.basket_update, name='update'),
]