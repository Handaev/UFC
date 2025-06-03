from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import OrderCreateForm
from .models import OrderItem
from basket.models import Basket, BasketItem
from catalog_product.models import Product

from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('created')
    return render(request, 'orders/list.html', {'orders': orders})


@login_required
def order_create(request):
    # Получаем корзину пользователя из базы данных
    try:
        basket = Basket.objects.get(user=request.user)
    except Basket.DoesNotExist:
        return redirect('basket:detail')  # Предполагается, что у вас есть URL с именем 'basket:detail'

    basket_items = basket.items.all()
    
    if not basket_items.exists():
        return redirect('basket:detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            
            # Рассчитываем общую сумму
            total_price = sum(item.total_price for item in basket_items)
            order.total_price = total_price
            order.save()
            
            # Создаем элементы заказа
            for item in basket_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.price,
                    quantity=item.quantity
                )
            
            # Очищаем корзину (удаляем все элементы)
            basket_items.delete()
            
            return render(request, 'orders/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    
    # Подготавливаем данные товаров для отображения
    product_list = []
    for item in basket_items:
        product_dict = {
            'object': item.product,
            'quantity': item.quantity,
            'price': item.price,
            'total': item.total_price
        }
        product_list.append(product_dict)
    
    total_price = sum(item['total'] for item in product_list)
    
    return render(request, 'orders/create.html', {
        'product_items': product_list,
        'total_price': total_price,
        'form': form
    })

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})