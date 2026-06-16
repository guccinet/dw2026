from django.contrib import admin
from .models import Coupon, LoyaltyPoint, Campaign

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'coupon_type', 'value', 'usage_limit', 'used_count', 'is_active', 'end_date')
    list_filter = ('coupon_type', 'is_active', 'start_date', 'end_date')
    search_fields = ('code',)
    ordering = ('-end_date',)

@admin.register(LoyaltyPoint)
class LoyaltyPointAdmin(admin.ModelAdmin):
    list_display = ('customer', 'points', 'accumulated_points', 'updated_at')
    search_fields = ('customer__user__username', 'customer__phone')
    ordering = ('-points',)

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('name', 'description')
    ordering = ('-start_date',)
