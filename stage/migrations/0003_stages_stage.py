# Generated by Django 4.2.2 on 2023-06-28 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stage', '0002_rename_stage_id_stages_line_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='stages',
            name='stage',
            field=models.CharField(choices=[('start', 'start'), ('end', 'end')], default='end', max_length=5),
        ),
    ]
