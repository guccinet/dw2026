from django.db import models
from django.contrib.auth.models import User
from storefront.models import Product

class Supplier(models.Model):
    name = models.CharField(max_length=255, verbose_name="ชื่อผู้จำหน่าย/ซัพพลายเออร์")
    contact_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="ผู้ติดต่อ")
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name="เบอร์โทรศัพท์")
    email = models.EmailField(blank=True, null=True, verbose_name="อีเมล")
    address = models.TextField(blank=True, null=True, verbose_name="ที่อยู่")

    class Meta:
        verbose_name = "ผู้จำหน่ายสินค้า (Supplier)"
        verbose_name_plural = "ข้อมูลผู้จำหน่ายสินค้า (Suppliers)"

    def __str__(self):
        return self.name

class SKU(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='skus', verbose_name="สินค้าหน้าเว็บ")
    sku_code = models.CharField(max_length=100, unique=True, verbose_name="รหัส SKU")
    color = models.CharField(max_length=50, blank=True, null=True, verbose_name="สี")
    size = models.CharField(max_length=50, blank=True, null=True, verbose_name="ขนาด")
    barcode = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name="บาร์โค้ด")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ราคาทุน (บาท)")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='skus', verbose_name="ผู้จัดจำหน่าย")

    class Meta:
        verbose_name = "รหัสสินค้าคลัง (SKU)"
        verbose_name_plural = "รหัสสินค้าคลัง (SKUs)"

    def __str__(self):
        attributes = []
        if self.color: attributes.append(self.color)
        if self.size: attributes.append(self.size)
        attr_str = f" ({', '.join(attributes)})" if attributes else ""
        return f"{self.product.name}{attr_str} - {self.sku_code}"

class Stock(models.Model):
    sku = models.OneToOneField(SKU, on_delete=models.CASCADE, related_name='stock', verbose_name="สินค้า SKU")
    quantity = models.IntegerField(default=0, verbose_name="จำนวนคงเหลือ")
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name="ตำแหน่งจัดวาง (Zone/Aisle/Shelf)")
    reorder_level = models.PositiveIntegerField(default=10, verbose_name="ระดับเตือนสต็อกต่ำ")
    last_counted_date = models.DateTimeField(auto_now=True, verbose_name="วันที่ตรวจสอบล่าสุด")

    class Meta:
        verbose_name = "จำนวนสินค้าคงคลัง"
        verbose_name_plural = "รายการสินค้าคงคลัง (Stock)"

    def __str__(self):
        return f"{self.sku.sku_code} - คงเหลือ {self.quantity} ชิ้น"

class StockAdjustment(models.Model):
    ADJUSTMENT_TYPES = (
        ('inbound', 'รับสินค้าเข้าคลัง (Inbound)'),
        ('outbound', 'จ่ายสินค้าออก (Outbound)'),
        ('audit', 'การตรวจนับคลัง (Audit Adjustment)'),
        ('damaged', 'สินค้าชำรุดเสียหาย (Damaged)'),
        ('returned', 'ลูกค้ารับคืนเข้าระบบ (Returned)'),
    )

    sku = models.ForeignKey(SKU, on_delete=models.CASCADE, related_name='adjustments', verbose_name="สินค้า SKU")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="ผู้ทำรายการ")
    adjustment_type = models.CharField(max_length=20, choices=ADJUSTMENT_TYPES, verbose_name="ประเภทการปรับปรุง")
    quantity_changed = models.IntegerField(verbose_name="จำนวนที่ปรับปรุง (+/-)")
    reason = models.TextField(blank=True, null=True, verbose_name="เหตุผลและรายละเอียด")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันเวลาที่ทำรายการ")

    class Meta:
        verbose_name = "ประวัติการปรับปรุงสต็อก"
        verbose_name_plural = "ประวัติการปรับปรุงสต็อก (Stock Adjustments)"

    def __str__(self):
        sign = "+" if self.quantity_changed >= 0 else ""
        return f"{self.sku.sku_code}: {self.get_adjustment_type_display()} ({sign}{self.quantity_changed})"
