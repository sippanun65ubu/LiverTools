from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),  # หน้าหลักไปที่ shop
    path('user/', include('user.urls')),  # จัดการบัญชีผู้ใช้
]

# เพิ่มเส้นทางสำหรับไฟล์มีเดีย (รูปภาพ)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)