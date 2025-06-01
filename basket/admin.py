from django.contrib import admin
from .models import Basket, BasketItem

class BasketItemInline(admin.TabularInline):
    model = BasketItem
    extra = 0

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    inlines = [BasketItemInline]
    list_display = ['user', 'created_at', 'updated_at']

@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ['basket', 'product', 'quantity', 'price']