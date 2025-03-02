# Generated by Django 5.1.6 on 2025-03-02 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_order_shipping_address_alter_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='shipping_address',
            new_name='address_line',
        ),
        migrations.AddField(
            model_name='order',
            name='zip_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
