# Generated by Django 5.0.6 on 2024-06-07 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_delete_uploadimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
