# Generated by Django 5.0.3 on 2024-04-10 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materialemagazzino',
            name='prov',
        ),
    ]
