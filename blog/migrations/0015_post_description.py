# Generated by Django 5.0.6 on 2024-06-11 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_rename_count_cartitems_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.CharField(default='No description given', max_length=200),
        ),
    ]