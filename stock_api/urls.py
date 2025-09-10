# stock_api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    ProductVariantViewSet,
    LocationViewSet,
    StockLevelViewSet,
    StockMovementCreateView
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'variants', ProductVariantViewSet, basename='productvariant')
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'stock-levels', StockLevelViewSet, basename='stocklevel')

# The API URLs are now determined automatically by the router.
# We also need to add the URL for our non-viewset view manually.
urlpatterns = [
    path('', include(router.urls)),
    path('stock-movements/', StockMovementCreateView.as_view(), name='create-stock-movement'),
]