from django.contrib import admin
from .models import Supplier, SKU, Stock, StockAdjustment

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_name', 'phone', 'email')
    search_fields = ('name', 'contact_name', 'phone', 'email')

@admin.register(SKU)
class SKUAdmin(admin.ModelAdmin):
    list_display = ('sku_code', 'product', 'color', 'size', 'barcode', 'cost_price', 'supplier')
    list_filter = ('supplier', 'color', 'size')
    search_fields = ('sku_code', 'product__name', 'barcode')
    raw_id_fields = ('product',)

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('sku', 'quantity', 'location', 'reorder_level', 'last_counted_date')
    list_filter = ('reorder_level',)
    search_fields = ('sku__sku_code', 'sku__product__name', 'location')
    ordering = ('quantity',)

@admin.register(StockAdjustment)
class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('sku', 'user', 'adjustment_type', 'quantity_changed', 'created_at')
    list_filter = ('adjustment_type', 'created_at')
    search_fields = ('sku__sku_code', 'sku__product__name', 'reason')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
