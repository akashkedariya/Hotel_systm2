# Generated by Django 4.2.14 on 2024-07-23 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_booking_cus_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='check_out',
            field=models.DateTimeField(default=''),
        ),
        migrations.AlterField(
            model_name='booking',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
