# Generated by Django 3.2.12 on 2023-05-02 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_order_orderitem_product_shippingaddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='digital',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
