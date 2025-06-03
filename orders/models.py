from django.db import models
from django.conf import settings
from catalog_product.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('in_progress', 'В обработке'),
        ('completed', 'Завершен'),
        ('canceled', 'Отменен'),
    ]
    
    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('card', 'Карта'),
        ('online', 'Онлайн оплата'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Контактные данные
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return f'Order {self.id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity