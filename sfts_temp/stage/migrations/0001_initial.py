# Generated by Django 4.2.3 on 2023-07-09 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ListOfStages',
            fields=[
                ('stageName', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='StageData',
            fields=[
                ('ipAddress', models.GenericIPAddressField(primary_key=True, serialize=False)),
                ('placeName', models.CharField(choices=[('start', 'start'), ('end', 'end'), ('qa', 'qa'), ('rework', 'rework')], max_length=6)),
                ('stageName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stage.listofstages')),
            ],
        ),
    ]
