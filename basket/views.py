from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Basket, BasketItem
from catalog_product.models import Product

@login_required
def basket_detail(request):
    basket = Basket.objects.get_or_create(user=request.user)[0]
    return render(request, 'basket/detail.html', {'basket': basket})

@login_required
def basket_add(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        basket, _ = Basket.objects.get_or_create(user=request.user)
        
        item = basket.get_item(product_id)
        
        if item:
            item.quantity += 1
            item.save()
        else:
            BasketItem.objects.create(
                basket=basket,
                product=product,
                price=product.price,
                quantity=1
            )
        
        messages.success(request, f'Товар "{product.name}" добавлен в корзину')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'total_quantity': basket.total_quantity,
                'total_price': basket.total_price
            })
        
        return redirect(request.META.get('HTTP_REFERER', 'catalog_product:product_list'))
    
    return redirect('catalog_product:product_list')

@login_required
def basket_remove(request, item_id):
    item = get_object_or_404(BasketItem, id=item_id, basket__user=request.user)
    product_name = item.product.name
    item.delete()
    messages.success(request, f'Товар "{product_name}" удален из корзины')
    return redirect('basket:detail')

@login_required
def basket_update(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(BasketItem, id=item_id, basket__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            item.quantity = quantity
            item.save()
            messages.success(request, 'Количество обновлено')
        else:
            item.delete()
            messages.success(request, 'Товар удален из корзины')
        
        return redirect('basket:detail')
    return redirect('basket:detail')

