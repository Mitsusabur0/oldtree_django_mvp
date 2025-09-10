# stock_api/views.py

from rest_framework import viewsets, generics
from .models import Product, ProductVariant, Location, StockLevel, StockMovement
from .serializers import (
    ProductSerializer,
    ProductVariantSerializer,
    LocationSerializer,
    StockLevelSerializer,
    StockMovementSerializer
)

# Create your views here.

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows products to be viewed.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductVariantViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows product variants to be viewed.
    """
    queryset = ProductVariant.objects.all().order_by('product__name', 'size', 'color')
    serializer_class = ProductVariantSerializer

class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows locations to be viewed.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class StockLevelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows current stock levels to be viewed.
    This is the primary endpoint for the frontend dashboard.
    """
    queryset = StockLevel.objects.select_related('product_variant', 'location', 'product_variant__product').all()
    serializer_class = StockLevelSerializer

class StockMovementCreateView(generics.CreateAPIView):
    """
    API endpoint for creating new stock movements.
    This is the primary WRITE endpoint for the application.
    Submitting data here will trigger the stock level update logic.
    """
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer