# Generated by Django 3.2.13 on 2023-07-23 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20230722_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='create',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
