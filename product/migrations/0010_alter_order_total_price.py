# Generated by Django 5.1.4 on 2025-02-13 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.IntegerField(null=True),
        ),
    ]
