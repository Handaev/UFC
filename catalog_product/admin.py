from django.contrib import admin
from django.utils.html import format_html
from import_export import resources, fields
from django.utils.html import strip_tags
from import_export.admin import ExportMixin
from .models import (
    Category, Brand, Fighter,
    Product, ProductImage,
    ProductSize
)



class ProductResource(resources.ModelResource):
    # Вычисляемое поле
    discount_percent = fields.Field(column_name='Скидка (%)')

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'old_price', 'discount_percent', 'category__name', 'brand__name')
        export_order = ('id', 'name', 'price', 'old_price', 'discount_percent', 'category__name', 'brand__name')

    # ✅ Метод 1: вычисляемое поле
    def get_discount_percent(self, obj):
        return obj.get_discount_percent()

    # ✅ Метод 2: деформация поля description (например, убираем HTML)
    def dehydrate_description(self, obj):
        return strip_tags(obj.description)[:100]  # Ограничим 100 символами

    # ✅ Метод 3: фильтрация queryset при экспорте (например, только активные товары)
    def get_export_queryset(self, request):
        return super().get_export_queryset(request).filter(is_active=True)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_main', 'order')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "-"

    preview.short_description = 'Превью'


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1
    fields = ('size', 'stock')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Изображение', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Логотип', {
            'fields': ('logo',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Fighter)
class FighterAdmin(admin.ModelAdmin):
    list_display = ('name', 'nickname', 'weight_class', 'country', 'is_active')
    list_filter = ('weight_class', 'country', 'is_active')
    search_fields = ('name', 'nickname')
    fieldsets = (
        (None, {
            'fields': ('name', 'nickname', 'is_active')
        }),
        ('Дополнительно', {
            'fields': ('weight_class', 'country'),
            'classes': ('collapse',)
        }),
        ('Изображение', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Product)
class ProductAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        'name', 'sku', 'price', 'old_price',
        'category', 'brand', 'is_active',
        'is_featured', 'is_bestseller', 'is_new'
    )
    list_filter = (
        'category', 'brand', 'is_active',
        'is_featured', 'is_bestseller', 'is_new'
    )
    resource_class = ProductResource
    search_fields = ('name', 'sku', 'description')
    filter_horizontal = ('fighters',)
    readonly_fields = ('created_at', 'updated_at', 'discount_percent')
    fieldsets = (
        (None, {
            'fields': ('name', 'sku', 'description', 'short_description')
        }),
        ('Цены', {
            'fields': ('price', 'old_price', 'discount_percent'),
            'classes': ('collapse',)
        }),
        ('Категории', {
            'fields': ('category', 'brand', 'fighters'),
            'classes': ('collapse',)
        }),
        ('Флаги', {
            'fields': ('is_featured', 'is_bestseller', 'is_new', 'is_active'),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def discount_percent(self, obj):
        return f"{obj.get_discount_percent()}%"

    discount_percent.short_description = 'Скидка'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'preview', 'is_main', 'order')
    list_filter = ('is_main',)
    search_fields = ('product__name',)
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return "-"

    preview.short_description = 'Превью'


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'stock')
    list_filter = ('size',)
    search_fields = ('product__name', 'size')