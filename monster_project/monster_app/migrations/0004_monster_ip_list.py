# Generated by Django 4.2.1 on 2023-06-15 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monster_app', '0003_gameentity_location_x_gameentity_location_y'),
    ]

    operations = [
        migrations.AddField(
            model_name='monster',
            name='ip_list',
            field=models.TextField(default='[]'),
        ),
    ]