# Generated by Django 5.0.6 on 2024-06-14 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_cart_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='date',
            new_name='date_placed',
        ),
    ]