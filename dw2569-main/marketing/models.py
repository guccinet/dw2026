from django.db import models
from storefront.models import Customer

class Coupon(models.Model):
    COUPON_TYPES = (
        ('percentage', 'ลดเป็นเปอร์เซ็นต์ (%)'),
        ('fixed', 'ลดเป็นจำนวนเงินสุทธิ (บาท)'),
        ('free_shipping', 'คูปองส่งฟรี'),
    )

    code = models.CharField(max_length=50, unique=True, verbose_name="รหัสคูปอง")
    coupon_type = models.CharField(max_length=20, choices=COUPON_TYPES, default='fixed', verbose_name="ประเภทส่วนลด")
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="มูลค่าส่วนลด (บาท หรือ %)")
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="ส่วนลดสูงสุด (เฉพาะแบบ %)")
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="ยอดสั่งซื้อขั้นต่ำ (บาท)")
    usage_limit = models.PositiveIntegerField(default=100, verbose_name="จำนวนสิทธิ์การใช้รวม")
    used_count = models.PositiveIntegerField(default=0, verbose_name="จำนวนที่ใช้ไปแล้ว")
    start_date = models.DateTimeField(verbose_name="วันที่เริ่มใช้งาน")
    end_date = models.DateTimeField(verbose_name="วันที่หมดอายุ")
    is_active = models.BooleanField(default=True, verbose_name="เปิดใช้งานคูปอง")

    class Meta:
        verbose_name = "คูปองส่วนลด"
        verbose_name_plural = "ข้อมูลคูปองส่วนลด"

    def __str__(self):
        return f"{self.code} - {self.get_coupon_type_display()} ({self.value})"

class LoyaltyPoint(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='loyalty_points', verbose_name="ลูกค้า")
    points = models.IntegerField(default=0, verbose_name="คะแนนสะสมคงเหลือ")
    accumulated_points = models.IntegerField(default=0, verbose_name="คะแนนสะสมทั้งหมดที่เคยได้รับ")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="อัปเดตล่าสุดเมื่อ")

    class Meta:
        verbose_name = "คะแนนสะสมลูกค้า"
        verbose_name_plural = "คะแนนสะสมของลูกค้า (Loyalty Points)"

    def __str__(self):
        return f"{self.customer.user.username} - คะแนนสะสม: {self.points} แต้ม"

class Campaign(models.Model):
    name = models.CharField(max_length=255, verbose_name="ชื่อแคมเปญการตลาด")
    description = models.TextField(blank=True, null=True, verbose_name="รายละเอียดแคมเปญ")
    banner_image = models.ImageField(upload_to='campaigns/', blank=True, null=True, verbose_name="ภาพแบนเนอร์แคมเปญ")
    start_date = models.DateTimeField(verbose_name="วันที่เริ่มแคมเปญ")
    end_date = models.DateTimeField(verbose_name="วันที่สิ้นสุดแคมเปญ")
    is_active = models.BooleanField(default=True, verbose_name="สถานะแคมเปญ (ใช้งาน/ปิดใช้งาน)")

    class Meta:
        verbose_name = "แคมเปญการตลาด"
        verbose_name_plural = "แคมเปญการตลาด (Campaigns)"

    def __str__(self):
        return self.name
