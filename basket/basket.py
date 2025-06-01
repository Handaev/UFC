from catalog_product.models import Product
from .models import Basket, BasketItem  # Импортируем модели корзины

def get_basket_items(request):
    """Возвращает список товаров в корзине пользователя"""
    if not request.user.is_authenticated:
        return []
    
    basket = Basket.objects.get_or_create(user=request.user)[0]
    basket_items = []
    
    for item in basket.items.all():  # Предполагается, что у Basket есть related_name='items'
        basket_items.append({
            'product': item.product,
            'quantity': item.quantity,
            'price': item.price,
            'total_price': item.quantity * item.price,
        })
    
    return basket_items