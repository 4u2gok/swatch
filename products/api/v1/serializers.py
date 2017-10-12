from rest_framework import serializers
from ...models import Product, ProductCategory, ProductOffer


class CompanyField(serializers.RelatedField):
    def to_representation(self, value):
        return value.short_name


class ProductCategoryField(serializers.RelatedField):
    def to_representation(self, value):
        return value.identifier

class ProductSerializer(serializers.ModelSerializer):
    company = CompanyField(read_only=True)
    category = ProductCategoryField()

    class Meta:
        model = Product
        fields = ('id', 'brand_name', 'company', 'content', 'category',
                  'strength', 'pack', 'mrp', 'updated_on', 'is_active',
                  'has_active_category_commission')


class ProductOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOffer
        fields = ('product', 'offer',)


class ActiveProductOfferSerializer(serializers.Serializer):
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    offers = ProductOfferSerializer(read_only=True, many=True)

    def validate_products(self, products):
        if not products:
            raise serializers.ValidationError('This list cannot be empty.')

        # Remove inactive Products
        products = [product for product in products if product.is_active]
        return products