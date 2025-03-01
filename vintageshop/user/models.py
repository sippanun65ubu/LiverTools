from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)  # ชื่อ-นามสกุล
    phone_number = models.CharField(max_length=15)  # เบอร์โทร
    email = models.EmailField(unique=True)  # อีเมล

    def __str__(self):
        return self.username
