
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    """Категория товаров (например, перчатки, футболки, шорты)"""
    name = models.CharField('Название', max_length=100, unique=True)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение', upload_to='categories/', blank=True)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name



class Brand(models.Model):
    """Бренд UFC или связанный с MMA"""
    name = models.CharField('Название', max_length=100, unique=True)
    description = models.TextField('Описание', blank=True)
    logo = models.ImageField('Логотип', upload_to='brands/', blank=True)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['name']

    def __str__(self):
        return self.name



class Fighter(models.Model):
    """Боец UFC, с которым может быть связан товар"""
    name = models.CharField('Имя', max_length=100)
    nickname = models.CharField('Прозвище', max_length=100, blank=True)
    weight_class = models.CharField('Весовая категория', max_length=50, blank=True)
    country = models.CharField('Страна', max_length=50, blank=True)
    image = models.ImageField('Фото', upload_to='fighters/', blank=True)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Боец'
        verbose_name_plural = 'Бойцы'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.nickname})" if self.nickname else self.name



class Product(models.Model):
    """Товар в каталоге"""
    name = models.CharField('Название', max_length=200)
    sku = models.CharField('Артикул', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True)
    short_description = models.CharField('Краткое описание', max_length=255, blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    old_price = models.DecimalField(
        'Старая цена',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True,
        blank=True
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        verbose_name='Бренд',
        null=True,
        blank=True
    )
    fighters = models.ManyToManyField(
        Fighter,
        verbose_name='Бойцы',
        blank=True
    )
    is_featured = models.BooleanField('Рекомендуемый', default=False)
    is_bestseller = models.BooleanField('Хит продаж', default=False)
    is_new = models.BooleanField('Новинка', default=False)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


    def get_discount_percent(self):
        """Возвращает процент скидки, если есть старая цена"""
        if self.old_price and self.old_price > self.price:
            return int((1 - self.price / self.old_price) * 100)
        return 0


class ProductImage(models.Model):
    """Изображения товара"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        related_name='images'
    )
    image = models.ImageField('Изображение', upload_to='products/')
    is_main = models.BooleanField('Основное изображение', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
        ordering = ['order']

    def __str__(self):
        return f"Изображение {self.product.name}"

    def save(self, *args, **kwargs):
        # Если это основное изображение, снимаем флаг у других изображений этого товара
        if self.is_main:
            ProductImage.objects.filter(product=self.product).exclude(id=self.id).update(is_main=False)
        super().save(*args, **kwargs)


class ProductSize(models.Model):
    """Размеры товара (для одежды, перчаток и т.д.)"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        related_name='sizes'
    )
    size = models.CharField('Размер', max_length=20)
    stock = models.PositiveIntegerField('Количество', default=0)

    class Meta:
        verbose_name = 'Размер товара'
        verbose_name_plural = 'Размеры товаров'
        unique_together = ('product', 'size')

    def __str__(self):
        return f"{self.product.name} - {self.size}"
