import django_filters
from rest_framework import filters
from ...models import Product


class ProductFilter(filters.FilterSet):
    is_active = django_filters.BooleanFilter(name="is_active")
    company = django_filters.CharFilter(name="company__short_name")
    updated_since = django_filters.IsoDateTimeFilter(name='updated_on', lookup_expr='gte')
    category = django_filters.CharFilter(name="category")

    class Meta:
        model = Product
        fields = ['is_active', 'company', 'updated_since', 'category']
