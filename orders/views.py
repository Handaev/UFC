from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OrderCreateForm
from basket.basket import get_basket_items
from .models import OrderItem


@login_required
def order_create(request):
    basket = request.session.get('basket', {})
    if not basket:
        return redirect('basket:detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            try:
                order = form.save(commit=False)
                order.user = request.user
                
                # Рассчитываем общую сумму
                total_price = 0
                for product_id, item in basket.items():
                    total_price += float(item['price']) * int(item['quantity'])
                order.total_price = total_price
                order.save()

                # Создаем элементы заказа
                for product_id, item in basket.items():
                    OrderItem.objects.create(
                        order=order,
                        product_id=product_id,  # Используем ключ словаря как product_id
                        price=item['price'],
                        quantity=item['quantity']
                    )
                
                # Очищаем корзину
                request.session['basket'] = {}
                request.session.modified = True
                
                return render(request, 'orders/created.html', {'order': order})
            
            except Exception as e:
                print(f"Error creating order: {e}")
                form.add_error(None, "Произошла ошибка при создании заказа")
    else:
        form = OrderCreateForm()

    return render(request, 'orders/create.html', {
        'basket': basket,
        'form': form
    })

@login_required
def order_create(request):
    basket_items = get_basket_items(request)  # Получаем сразу список товаров
    if not basket_items:  # Проверяем пустую корзину
        return redirect('basket:detail')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            # Нужно пересчитать total_price на основе basket_items
            order.total_price = sum(item['price'] * item['quantity'] for item in basket_items)
            order.save()
            
            for item in basket_items:  
                OrderItem.objects.create(
                    order=order,
                    product_id=item['product_id'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # Очистка корзины (нужно реализовать)
            request.session['basket'] = {}
            return render(request, 'orders/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    
    return render(request, 'orders/create.html', {
        'basket_items': basket_items,  # Просто передаем список товаров
        'form': form
    })