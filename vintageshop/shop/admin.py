from django.contrib import admin
from .models import Product  # นำเข้า Model ของสินค้า

# ลงทะเบียน Model Product ให้แสดงในหน้า Admin
admin.site.register(Product)
