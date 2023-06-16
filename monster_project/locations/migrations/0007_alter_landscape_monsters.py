# Generated by Django 4.2.1 on 2023-06-16 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monster_app', '0004_monster_ip_list'),
        ('locations', '0006_landscape_monsters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landscape',
            name='monsters',
            field=models.ManyToManyField(blank=True, to='monster_app.monster'),
        ),
    ]