# Generated by Django 4.2.11 on 2024-03-08 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_materiale_movimenti_remove_book_author_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movimenti',
            name='data_movimento',
        ),
    ]