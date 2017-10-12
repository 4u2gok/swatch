from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Product, ProductCategoryCommission, ProductOffer



def get_products():
    """
    Returns products queryset
    """
    return Product.objects.all()


def get_active_productcat_commisions():
    """
    Returns ProductCategoryCommission records that are currently active
    """
    return ProductCategoryCommission.objects.filter(
        valid_from__lte=timezone.now(),
        valid_to__gte=timezone.now(),
        is_active=True
    ).order_by('-valid_from', 'valid_to').only('product_category', 'commission_percentage')\
    .select_related('product_category')


def get_active_offers(products=None):
    """
    Returns the queryset of active offers
    """
    if not products:
        raise ValidationError('Product id list cannot be empty.')

    return ProductOffer.objects.filter(
        product__in=products,
        valid_from__lte=timezone.now(),
        valid_to__gte=timezone.now(),
        is_active=True
    )