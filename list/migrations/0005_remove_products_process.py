# Generated by Django 4.2.2 on 2023-06-23 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0004_alter_products_fg_code_alter_products_product_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='process',
        ),
    ]
