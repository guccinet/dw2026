from django.shortcuts import render
from .models import ShippingMethod, Delivery, ReturnRequest

def index(request):
    methods = ShippingMethod.objects.all()
    deliveries = Delivery.objects.all().order_by('-last_updated')
    returns = ReturnRequest.objects.all().order_by('-created_at')
    
    # Calculate some dashboard summaries
    total_deliveries = deliveries.count()
    pending_deliveries = deliveries.filter(status='pending').count()
    in_transit_count = deliveries.filter(status='in_transit').count()
    delivered_count = deliveries.filter(status='delivered').count()
    
    context = {
        'methods': methods,
        'deliveries': deliveries,
        'returns': returns,
        'total_deliveries': total_deliveries,
        'pending_deliveries': pending_deliveries,
        'in_transit_count': in_transit_count,
        'delivered_count': delivered_count,
    }
    return render(request, 'logistics/index.html', context)
