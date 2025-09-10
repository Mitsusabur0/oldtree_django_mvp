from django.db import models, transaction 
from django.core.validators import MinValueValidator

# Create your models here.

class Product(models.Model):
    """
    Stores base product information.
    e.g., "T-Shirt Classic", "SKU-TSHIRT"
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    base_sku = models.CharField(max_length=100, unique=True, help_text="Base Stock Keeping Unit for the product line.")

    def __str__(self):
        return f"{self.name} ({self.base_sku})"

class ProductVariant(models.Model):
    """
    Links to a Product and stores specific variations.
    This is the actual item we track in inventory.
    e.g., T-Shirt Classic, Size M, Color Blue, SKU-TSHIRT-M-BLU
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    unique_sku = models.CharField(max_length=100, unique=True, help_text="Unique SKU for this specific variant.")
    
    class Meta:
        # Ensures that each combination of product, size, and color is unique.
        unique_together = ('product', 'size', 'color')

    def __str__(self):
        return f"{self.product.name} - Size: {self.size}, Color: {self.color} ({self.unique_sku})"

class Location(models.Model):
    """
    Stores the different places stock can be.
    e.g., "Tienda Física", "Bodega Principal"
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class StockLevel(models.Model):
    """
    The core table connecting a ProductVariant to a Location with a quantity.
    This represents the actual inventory count at a specific place.
    """
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        # Ensures we only have one stock level entry per variant per location.
        unique_together = ('product_variant', 'location')

    def __str__(self):
        return f"{self.product_variant.unique_sku} at {self.location.name}: {self.quantity}"

class StockMovement(models.Model):
    """
    A log table to record every transaction or change in stock.
    This provides an auditable history of all inventory changes.
    """
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    quantity_change = models.IntegerField() # Can be positive (restock) or negative (sale)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=255, blank=True, null=True, help_text="e.g., 'Venta Tienda Física, boleta #1234' or 'Ajuste de inventario'")

    def __str__(self):
        return f"Movement of {self.quantity_change} for {self.product_variant.unique_sku} at {self.location.name} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    # --- THIS IS THE CORE BUSINESS LOGIC ---
    def save(self, *args, **kwargs):
        # Use a database transaction to ensure data integrity.
        with transaction.atomic():
            # Get or create the corresponding stock level.
            # This handles cases where we're adding stock for a variant in a location for the first time.
            stock_level, created = StockLevel.objects.get_or_create(
                product_variant=self.product_variant,
                location=self.location,
                defaults={'quantity': 0}
            )

            # Update the quantity.
            stock_level.quantity += self.quantity_change
            stock_level.save()

            # Finally, save the StockMovement instance itself.
            super().save(*args, **kwargs)