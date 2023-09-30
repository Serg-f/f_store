# Generated by Django 3.2.13 on 2023-09-20 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_emailverification_expiration'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(default='Hauptstrasse 88', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female')], default='m', max_length=1),
        ),
    ]