from django.shortcuts import render
from .models import Coupon, LoyaltyPoint, Campaign

def index(request):
    coupons = Coupon.objects.all()
    campaigns = Campaign.objects.all()
    points = LoyaltyPoint.objects.all().order_by('-points')
    
    # Calculate some dashboard summaries
    active_coupons = coupons.filter(is_active=True).count()
    active_campaigns = campaigns.filter(is_active=True).count()
    
    context = {
        'coupons': coupons,
        'campaigns': campaigns,
        'points': points,
        'active_coupons': active_coupons,
        'active_campaigns': active_campaigns,
    }
    return render(request, 'marketing/index.html', context)
