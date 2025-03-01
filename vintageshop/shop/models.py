from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES)
    
    # Change from a single ForeignKey to a ManyToManyField
    category = models.ManyToManyField(Category, blank=True)
    
    image = models.ImageField(upload_to='products/', blank=True)

    def __str__(self):
        return self.name
