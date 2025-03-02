from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)  # ชื่อ-นามสกุล
    phone_number = models.CharField(max_length=15)  # เบอร์โทร
    email = models.EmailField(unique=True)  # อีเมล

    address = models.TextField(blank=True, null=True)  # ที่อยู่ (เป็นค่าว่างได้)
    zip_code = models.CharField(max_length=10, blank=True, null=True)  # รหัสไปรษณีย์ (เป็นค่าว่างได้)

    USERNAME_FIELD = "email"  # ✅ ใช้อีเมลเป็นตัวล็อกอินแทน
    REQUIRED_FIELDS = ["username", "full_name", "phone_number"]

    def __str__(self):
        return self.email  # ✅ เปลี่ยนให้แสดงอีเมลแทน
    

class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="addresses"    
    )
    address_line = models.TextField(verbose_name="ที่อยู่")
    zip_code = models.CharField(max_length=10, verbose_name="รหัสไปรษณีย์")
    # You can add extra fields if needed (e.g., city, province, etc.)

    def __str__(self):
        return f"Address #{self.id} for {self.user.email}"