import os
import django
from django.utils import timezone
from datetime import timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guccinet.settings')
django.setup()

from django.contrib.auth.models import User
from storefront.models import Customer, Product, Order, OrderItem, Review
from inventory.models import Supplier, SKU, Stock, StockAdjustment
from marketing.models import Coupon, LoyaltyPoint, Campaign
from logistics.models import ShippingMethod, Delivery, ReturnRequest

def seed():
    print("Starting database seeding...")
    
    # 1. Create superuser if it doesn't exist (handled by command, but let's make a normal user too)
    user, _ = User.objects.get_or_create(
        username="premium_buyer",
        defaults={
            'email': "buyer@guccinet.com",
            'first_name': "สมชาย",
            'last_name': "หรูหรา"
        }
    )
    user.set_password("buyer12345")
    user.save()

    # 2. Create customer profile
    customer, _ = Customer.objects.get_or_create(
        user=user,
        defaults={
            'phone': "081-234-5678",
            'address': "123/45 ถนนวิทยุ แขวงลุมพินี เขตปทุมวัน กรุงเทพฯ 10330"
        }
    )
    print("- Created Customer")

    # 3. Create a supplier
    supplier, _ = Supplier.objects.get_or_create(
        name="Gucci Hub Italy",
        contact_name="Giovanni Rossi",
        phone="+39 02 8888 8888",
        email="supplier@guccinet.com",
        address="Florence, Tuscany, Italy"
    )
    print("- Created Supplier")

    # 4. Create products
    prod1, _ = Product.objects.get_or_create(
        name="Gucci Signature Leather Jacket",
        slug="gucci-signature-leather-jacket",
        defaults={
            'description': "แจ็คเก็ตหนังแท้คุณภาพสูง ตกแต่งด้วยโลโก้ Double G แบบนูนอันเป็นเอกลักษณ์ของแบรนด์ ออกแบบมาเพื่อสไตล์ที่หรูหราและร่วมสมัย",
            'price': 125000.00,
            'is_active': True
        }
    )
    
    prod2, _ = Product.objects.get_or_create(
        name="Gucci Canvas Backpack",
        slug="gucci-canvas-backpack",
        defaults={
            'description': "กระเป๋าเป้ผ้าแคนวาสลายโมโนแกรม GG ตกแต่งด้วยแถบสีเขียว-แดงสไตล์วินเทจ ด้านในบุหนังแท้ มีช่องจัดเก็บของขนาดใหญ่",
            'price': 68000.00,
            'is_active': True
        }
    )
    print("- Created Products")

    # 5. Create SKUs and Stock
    sku1, _ = SKU.objects.get_or_create(
        product=prod1,
        sku_code="GC-JCK-L-BLK",
        defaults={
            'color': "Black",
            'size': "L",
            'barcode': "8801234567890",
            'cost_price': 65000.00,
            'supplier': supplier
        }
    )
    
    sku2, _ = SKU.objects.get_or_create(
        product=prod2,
        sku_code="GC-BPK-OS-BRW",
        defaults={
            'color': "Brown",
            'size': "One Size",
            'barcode': "8801234567891",
            'cost_price': 32000.00,
            'supplier': supplier
        }
    )
    print("- Created SKUs")

    # Initialize Stock for SKUs
    stock1, _ = Stock.objects.get_or_create(
        sku=sku1,
        defaults={
            'quantity': 25,
            'location': "Zone A-Shelf 4",
            'reorder_level': 5
        }
    )
    stock2, _ = Stock.objects.get_or_create(
        sku=sku2,
        defaults={
            'quantity': 3,  # Set low to trigger "Low Stock" warning
            'location': "Zone B-Shelf 12",
            'reorder_level': 5
        }
    )
    print("- Initialized Stock")

    # 6. Create Shipping Methods
    ship1, _ = ShippingMethod.objects.get_or_create(
        name="Flash Express (Standard)",
        defaults={
            'base_rate': 45.00,
            'weight_limit': 15.00,
            'estimated_days': "1-2 วัน",
            'is_active': True
        }
    )
    ship2, _ = ShippingMethod.objects.get_or_create(
        name="Kerry Express (Premium)",
        defaults={
            'base_rate': 60.00,
            'weight_limit': 20.00,
            'estimated_days': "1 วัน",
            'is_active': True
        }
    )
    print("- Created Shipping Methods")

    # 7. Create Marketing Coupons
    Coupon.objects.get_or_create(
        code="GUCCISTART",
        defaults={
            'coupon_type': "fixed",
            'value': 1000.00,
            'min_purchase_amount': 20000.00,
            'usage_limit': 500,
            'start_date': timezone.now(),
            'end_date': timezone.now() + timedelta(days=365),
            'is_active': True
        }
    )
    Coupon.objects.get_or_create(
        code="GUCCIVIP10",
        defaults={
            'coupon_type': "percentage",
            'value': 10.00,
            'max_discount': 5000.00,
            'min_purchase_amount': 30000.00,
            'usage_limit': 100,
            'start_date': timezone.now(),
            'end_date': timezone.now() + timedelta(days=90),
            'is_active': True
        }
    )
    print("- Created Coupons")

    # 8. Create Campaigns
    Campaign.objects.get_or_create(
        name="Gucci Mid-Year Grand Sale 2026",
        defaults={
            'description': "แคมเปญลดราคาสินค้าแฟชั่นต้อนรับกลางปี รับส่วนลดสุดพิเศษและคะแนนสะสมคูณสองเมื่อมียอดชำระผ่าน PromptPay",
            'start_date': timezone.now(),
            'end_date': timezone.now() + timedelta(days=30),
            'is_active': True
        }
    )
    print("- Created Campaigns")

    # 9. Create Customer Loyalty Points
    LoyaltyPoint.objects.get_or_create(
        customer=customer,
        defaults={
            'points': 1250,
            'accumulated_points': 1500
        }
    )
    print("- Created Loyalty Points")

    # 10. Create Orders and OrderItems
    order1, _ = Order.objects.get_or_create(
        order_number="ORD20260616-001",
        defaults={
            'customer': customer,
            'total_amount': 125000.00,
            'status': 'shipped'
        }
    )
    
    OrderItem.objects.get_or_create(
        order=order1,
        product=prod1,
        defaults={
            'quantity': 1,
            'price': 125000.00
        }
    )
    print("- Created Orders & Order Items")

    # 11. Create Delivery for Order
    Delivery.objects.get_or_create(
        order=order1,
        defaults={
            'shipping_method': ship2,
            'tracking_number': "KER9998887776",
            'status': 'in_transit',
            'recipient_name': "คุณสมชาย หรูหรา",
            'recipient_phone': "081-234-5678",
            'shipping_address': "123/45 ถนนวิทยุ แขวงลุมพินี เขตปทุมวัน กรุงเทพฯ 10330",
            'shipped_at': timezone.now() - timedelta(hours=5)
        }
    )
    print("- Created Deliveries")

    # 12. Create a Stock Adjustment log
    StockAdjustment.objects.get_or_create(
        sku=sku2,
        adjustment_type='audit',
        defaults={
            'quantity_changed': -2,
            'reason': "ปรับลดยอดหลังจากสุ่มตรวจนับสต็อกประจำสัปดาห์ในโซน B"
        }
    )
    print("- Created Stock Adjustments")

    # 13. Create a Return Request
    # We create a second order that has failed or is returned
    order2, _ = Order.objects.get_or_create(
        order_number="ORD20260616-002",
        defaults={
            'customer': customer,
            'total_amount': 68000.00,
            'status': 'delivered'
        }
    )
    OrderItem.objects.get_or_create(
        order=order2,
        product=prod2,
        defaults={
            'quantity': 1,
            'price': 68000.00
        }
    )
    ReturnRequest.objects.get_or_create(
        order=order2,
        defaults={
            'reason': "ขนาดกระเป๋าแคนวาสไม่ตรงตามที่ต้องการและพบตำหนิตรงซิปด้านใน",
            'status': 'pending'
        }
    )
    print("- Created Return Requests")
    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed()
