# Generated by Django 5.0.6 on 2024-06-10 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_delete_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='stock',
            field=models.IntegerField(default=0),
        ),
    ]
