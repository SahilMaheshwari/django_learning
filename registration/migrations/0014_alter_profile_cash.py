# Generated by Django 5.0.6 on 2024-06-09 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0013_profile_cash_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cash',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
