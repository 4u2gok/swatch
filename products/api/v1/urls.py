"""
Products API V1 URLS are defined here
/api/v1/products/...
"""
from django.conf.urls import url
from .views import ProductListView, ProductDetailView, ActiveProductOfferView

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='product_list'),
    url(r'^(?P<id>\d{1,})$', ProductDetailView.as_view(), name='product_detail'),
    url(r'^offers/', ActiveProductOfferView.as_view(), name='offers_list')
]