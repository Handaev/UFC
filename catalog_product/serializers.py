from rest_framework import serializers
from .models import Category, Brand, Fighter, Product, ProductImage, ProductSize


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class FighterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fighter
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    sizes = ProductSizeSerializer(many=True, read_only=True)
    fighters = serializers.PrimaryKeyRelatedField(queryset=Fighter.objects.all(), many=True)

    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        price = data.get('price')
        old_price = data.get('old_price')

        if old_price is not None and price is not None and old_price <= price:
            raise serializers.ValidationError(
                "Старая цена должна быть больше текущей цены (иначе скидка некорректна)."
            )
        return data
