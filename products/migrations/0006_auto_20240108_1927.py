# Generated by Django 3.2.13 on 2024-01-08 18:27

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_stripe_price_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['image']},
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
