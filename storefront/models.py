from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile', verbose_name="ผู้ใช้งาน")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="เบอร์โทรศัพท์")
    address = models.TextField(blank=True, null=True, verbose_name="ที่อยู่สำหรับจัดส่ง")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "ลูกค้า"
        verbose_name_plural = "ข้อมูลลูกค้า"

    def __str__(self):
        return f"{self.user.username} ({self.user.get_full_name() or 'ไม่ระบุชื่อ'})"

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="ชื่อสินค้า")
    slug = models.SlugField(unique=True, verbose_name="สลัก (URL Slug)")
    description = models.TextField(blank=True, null=True, verbose_name="รายละเอียดสินค้า")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ราคา (บาท)")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="รูปภาพสินค้า")
    is_active = models.BooleanField(default=True, verbose_name="แสดงบนหน้าเว็บ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "สินค้า"
        verbose_name_plural = "สินค้าหน้าเว็บ"

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'รอการชำระเงิน'),
        ('paid', 'ชำระเงินแล้ว'),
        ('processing', 'กำลังจัดเตรียมสินค้า'),
        ('shipped', 'จัดส่งแล้ว'),
        ('delivered', 'จัดส่งสำเร็จ'),
        ('cancelled', 'ยกเลิกคำสั่งซื้อ'),
    )
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name="ลูกค้า")
    order_number = models.CharField(max_length=50, unique=True, verbose_name="เลขที่ใบสั่งซื้อ")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="ยอดสุทธิ")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="สถานะใบสั่งซื้อ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สั่งซื้อ")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "คำสั่งซื้อ"
        verbose_name_plural = "รายการคำสั่งซื้อ"

    def __str__(self):
        return f"Order {self.order_number} ({self.get_status_display()})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="คำสั่งซื้อ")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items', verbose_name="สินค้า")
    quantity = models.PositiveIntegerField(default=1, verbose_name="จำนวน")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ราคา ณ วันสั่งซื้อ")

    class Meta:
        verbose_name = "รายการสินค้าในคำสั่งซื้อ"
        verbose_name_plural = "รายการสินค้าในคำสั่งซื้อ"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="สินค้า")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews', verbose_name="ลูกค้า")
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="คะแนน")
    comment = models.TextField(blank=True, null=True, verbose_name="ความคิดเห็น")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "รีวิวสินค้า"
        verbose_name_plural = "รีวิวสินค้า"
        unique_together = ('product', 'customer')

    def __str__(self):
        return f"Review by {self.customer.user.username} - {self.rating} ดาว"
