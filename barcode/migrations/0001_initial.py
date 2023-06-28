# Generated by Django 4.2.2 on 2023-06-27 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('list', '0008_rename_name_products_product_name'),
        ('stage', '0002_rename_stage_id_stages_line_code'),
        ('session', '0003_alter_userlog_login_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermanentTrace',
            fields=[
                ('permanent_sno', models.CharField(max_length=13, null=True)),
                ('sno', models.CharField(max_length=12, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Rejection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('description', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Rework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('description', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Trace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('description', models.CharField(max_length=13)),
                ('product_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='list.products')),
                ('sno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='barcode.permanenttrace')),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stage.stagedata')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='session.userdata')),
            ],
        ),
    ]