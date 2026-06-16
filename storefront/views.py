from django.shortcuts import render
from .models import Product
from marketing.models import Coupon, Campaign

def index(request):
    products = Product.objects.filter(is_active=True)
    coupons = Coupon.objects.filter(is_active=True)
    campaigns = Campaign.objects.filter(is_active=True)
    
    context = {
        'products': products,
        'coupons': coupons,
        'campaigns': campaigns,
    }
    return render(request, 'storefront/index.html', context)
