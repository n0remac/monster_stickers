# Generated by Django 4.2.1 on 2023-06-13 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monster_app', '0003_gameentity_location_x_gameentity_location_y'),
        ('explore', '0003_alter_story_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adventure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('location_x', models.IntegerField(default=0)),
                ('location_y', models.IntegerField(default=0)),
                ('monster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adventure_monster', to='monster_app.monster')),
            ],
        ),
    ]