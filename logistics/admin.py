from django.contrib import admin
from .models import ShippingMethod, Delivery, ReturnRequest

@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_rate', 'weight_limit', 'estimated_days', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'shipping_method', 'tracking_number', 'status', 'recipient_name', 'last_updated')
    list_filter = ('status', 'shipping_method', 'last_updated')
    search_fields = ('order__order_number', 'tracking_number', 'recipient_name', 'recipient_phone')
    ordering = ('-last_updated',)
    readonly_fields = ('last_updated',)

@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'tracking_number', 'created_at', 'resolved_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order__order_number', 'tracking_number', 'reason')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
