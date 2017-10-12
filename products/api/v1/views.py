from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ...services import get_products, get_active_offers
from .filters import ProductFilter
from .serializers import ProductSerializer, ActiveProductOfferSerializer


class ProductListView(ListAPIView):
    """
    Returns list of products. List may be filtered using query parameters
    """
    queryset = get_products()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = ProductFilter


class ProductDetailView(RetrieveAPIView):
    """
    Returns details of a product.
    """
    queryset = get_products()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'


class ActiveProductOfferView(GenericAPIView):
    """
    Returns the list of active offers for products
    """
    serializer_class = ActiveProductOfferSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        products = serializer.validated_data['products']
        active_offers = get_active_offers(products=products)
        serializer._validated_data['offers'] = active_offers
        return Response(serializer.data)

