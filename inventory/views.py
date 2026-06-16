from django.shortcuts import render
from .models import SKU, Stock, StockAdjustment

def index(request):
    skus = SKU.objects.all()
    stocks = Stock.objects.all()
    adjustments = StockAdjustment.objects.all().order_index = StockAdjustment.objects.all().order_by('-created_at')[:10]
    
    # Calculate some summary stats
    total_skus = skus.count()
    low_stock_count = 0
    total_items = 0
    for stock in stocks:
        total_items += stock.quantity
        if stock.quantity <= stock.reorder_level:
            low_stock_count += 1

    context = {
        'skus': skus,
        'stocks': stocks,
        'adjustments': adjustments,
        'total_skus': total_skus,
        'low_stock_count': low_stock_count,
        'total_items': total_items,
    }
    return render(request, 'inventory/index.html', context)
