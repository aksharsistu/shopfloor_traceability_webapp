# Generated by Django 4.2.2 on 2023-06-23 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0005_remove_products_process'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='process',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='list.processes'),
        ),
    ]
