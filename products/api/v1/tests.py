from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.urlresolvers import resolve
from django.utils import timezone
from allauth.account.models import EmailAddress
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status
from .views import ProductListView, ProductDetailView
from ...models import Company, Product


class ProductListTests(APITestCase):
    def test_resolves_to_productlistview(self):
        match = resolve('/api/v1/products/')
        self.assertEqual(match.func.func_name, ProductListView.__name__)


class ProductDetailTests(APITestCase):
    def test_resolves_to_productdetailview(self):
        match = resolve('/api/v1/products/12')
        self.assertEqual(match.func.func_name, ProductDetailView.__name__)
        self.assertEqual(match.kwargs['id'], '12')












