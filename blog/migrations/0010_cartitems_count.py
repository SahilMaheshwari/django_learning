# Generated by Django 5.0.6 on 2024-06-10 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_cart_cartitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]