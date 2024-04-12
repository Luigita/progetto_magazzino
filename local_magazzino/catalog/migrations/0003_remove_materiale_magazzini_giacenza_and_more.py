# Generated by Django 5.0.3 on 2024-04-10 15:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_remove_materialemagazzino_prov'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materiale',
            name='magazzini_giacenza',
        ),
        migrations.RemoveField(
            model_name='materialemagazzino',
            name='materiale',
        ),
        migrations.AddField(
            model_name='materialemagazzino',
            name='movimenti',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='new_movimenti', to='catalog.movimenti'),
        ),
        migrations.AddField(
            model_name='movimenti',
            name='magazzini_giacenza',
            field=models.ManyToManyField(blank=True, through='catalog.MaterialeMagazzino', to='catalog.magazzino'),
        ),
    ]