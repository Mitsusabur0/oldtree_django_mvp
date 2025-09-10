# stock_api/serializers.py

from rest_framework import serializers
from .models import Product, ProductVariant, Location, StockLevel, StockMovement

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductVariantSerializer(serializers.ModelSerializer):
    # To make the API more readable, we'll show the product's name
    # instead of just its ID.
    product = serializers.StringRelatedField()

    class Meta:
        model = ProductVariant
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class StockLevelSerializer(serializers.ModelSerializer):
    """
    This serializer is designed for READ-ONLY purposes.
    It provides a detailed, nested representation of the stock level,
    which is perfect for displaying data on the frontend.
    """
    # Using nested serializers provides rich, contextual data in one API call.
    product_variant = ProductVariantSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = StockLevel
        fields = ['id', 'product_variant', 'location', 'quantity']


class StockMovementSerializer(serializers.ModelSerializer):
    """
    This serializer is designed for WRITE operations.
    It accepts simple primary key IDs for product_variant and location,
    which is exactly what we'll get from the frontend form submission.
    """
    class Meta:
        model = StockMovement
        fields = ['id', 'product_variant', 'location', 'quantity_change', 'notes', 'timestamp']
        # 'timestamp' is read-only because it's set automatically by the model.
        read_only_fields = ['timestamp']