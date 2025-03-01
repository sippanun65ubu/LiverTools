from django.db import models

class Product(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]

    CATEGORY_CHOICES = [
        ('parody', 'เสื้อล้อเลียน'),
        ('rare', 'งานแรร์'),
        ('artist', 'ศิลปิน'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="parody"  # เพิ่มค่า default
)
    image = models.ImageField(upload_to='products/', blank=True)

    def __str__(self):
        return self.name
