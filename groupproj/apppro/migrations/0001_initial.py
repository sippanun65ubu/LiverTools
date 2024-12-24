# Generated by Django 5.1.4 on 2024-12-24 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField()),
                ('occupation', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('habit_name', models.CharField(max_length=100)),
                ('frequency', models.CharField(choices=[('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly'), ('Twice a Week', 'Twice a Week')], max_length=50)),
                ('duration_minutes', models.PositiveIntegerField()),
                ('goal', models.CharField(max_length=255)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habits', to='apppro.person')),
            ],
        ),
    ]
