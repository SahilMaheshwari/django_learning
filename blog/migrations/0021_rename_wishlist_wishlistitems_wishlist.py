# Generated by Django 5.0.6 on 2024-06-14 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_wishlist_wishlistitems'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wishlistitems',
            old_name='Wishlist',
            new_name='wishlist',
        ),
    ]