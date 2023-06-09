# Generated by Django 4.2.1 on 2023-05-24 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('monster_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Battle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('battle_date', models.DateTimeField(auto_now_add=True)),
                ('attacker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attacker_monsters', to='monster_app.monster')),
                ('defender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='defender_monsters', to='monster_app.monster')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='winner_monsters', to='monster_app.monster')),
            ],
        ),
    ]
