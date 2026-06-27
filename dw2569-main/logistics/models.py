from django.db import models
from storefront.models import Order

class ShippingMethod(models.Model):
    name = models.CharField(max_length=100, verbose_name="ผู้บริการขนส่ง (เช่น Flash, Kerry)")
    base_rate = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="ค่าจัดส่งเริ่มต้น (บาท)")
    weight_limit = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="น้ำหนักสูงสุดที่รับได้ (กก.)")
    estimated_days = models.CharField(max_length=50, verbose_name="ระยะเวลาจัดส่งโดยประมาณ (วัน)")
    is_active = models.BooleanField(default=True, verbose_name="เปิดให้บริการ")

    class Meta:
        verbose_name = "วิธีการจัดส่ง"
        verbose_name_plural = "ผู้บริการขนส่งสินค้า"

    def __str__(self):
        return f"{self.name} (ค่าส่ง {self.base_rate} บาท)"

class Delivery(models.Model):
    DELIVERY_STATUS = (
        ('pending', 'รอจัดส่ง (Pending)'),
        ('in_transit', 'อยู่ระหว่างการขนส่ง (In Transit)'),
        ('out_for_delivery', 'พัสดุอยู่ระหว่างนำจ่าย (Out for Delivery)'),
        ('delivered', 'จัดส่งเรียบร้อยแล้ว (Delivered)'),
        ('failed', 'การจัดส่งล้มเหลว/ติดต่อไม่ได้ (Failed)'),
        ('returned', 'พัสดุตีกลับต้นทาง (Returned)'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery_info', verbose_name="คำสั่งซื้อ")
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True, related_name='deliveries', verbose_name="วิธีการจัดส่ง")
    tracking_number = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name="เลขติดตามพัสดุ (Tracking Number)")
    status = models.CharField(max_length=25, choices=DELIVERY_STATUS, default='pending', verbose_name="สถานะการนำส่งพัสดุ")
    recipient_name = models.CharField(max_length=255, verbose_name="ชื่อผู้รับปลายทาง")
    recipient_phone = models.CharField(max_length=50, verbose_name="เบอร์โทรศัพท์ติดต่อ")
    shipping_address = models.TextField(verbose_name="ที่อยู่จัดส่งจริง")
    shipped_at = models.DateTimeField(blank=True, null=True, verbose_name="เวลาส่งออกจากคลัง")
    delivered_at = models.DateTimeField(blank=True, null=True, verbose_name="เวลาจัดส่งสำเร็จ")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="อัปเดตสถานะล่าสุด")

    class Meta:
        verbose_name = "ข้อมูลการจัดส่งสินค้า"
        verbose_name_plural = "ข้อมูลการจัดส่งสินค้า (Deliveries)"

    def __str__(self):
        tracking = self.tracking_number or "รอออกเลข"
        return f"Order {self.order.order_number} via {self.shipping_method.name if self.shipping_method else 'N/A'} - [{tracking}]"

class ReturnRequest(models.Model):
    RETURN_STATUS = (
        ('pending', 'รอตรวจสอบคำขอ (Pending)'),
        ('approved', 'อนุมัติการคืนสินค้า (Approved)'),
        ('received', 'ได้รับพัสดุคืนแล้ว (Received)'),
        ('rejected', 'ปฏิเสธคำขอคืน (Rejected)'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='return_requests', verbose_name="คำสั่งซื้อ")
    reason = models.TextField(verbose_name="เหตุผลและคำอธิบายการคืน")
    status = models.CharField(max_length=20, choices=RETURN_STATUS, default='pending', verbose_name="สถานะการคืนสินค้า")
    tracking_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="เลขส่งคืนพัสดุของลูกค้า")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันเวลาขอคืนสินค้า")
    resolved_at = models.DateTimeField(blank=True, null=True, verbose_name="วันเวลาดำเนินการสิ้นสุด")

    class Meta:
        verbose_name = "รายการคืนสินค้า"
        verbose_name_plural = "รายการขอคืนสินค้า (Returns)"

    def __str__(self):
        return f"Return Request: Order {self.order.order_number} ({self.get_status_display()})"
