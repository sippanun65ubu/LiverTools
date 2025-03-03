# Generated by Django 5.1.6 on 2025-03-01 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("quantity", models.IntegerField(default=1)),
                (
                    "size",
                    models.CharField(
                        choices=[
                            ("S", "Small"),
                            ("M", "Medium"),
                            ("L", "Large"),
                            ("XL", "Extra Large"),
                            ("XXL", "Double Extra Large"),
                        ],
                        max_length=3,
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("parody", "เสื้อล้อเลียน"),
                            ("rare", "งานแรร์"),
                            ("artist", "ศิลปิน"),
                        ],
                        default="parody",
                        max_length=50,
                    ),
                ),
                ("image", models.ImageField(blank=True, upload_to="products/")),
            ],
        ),
    ]
