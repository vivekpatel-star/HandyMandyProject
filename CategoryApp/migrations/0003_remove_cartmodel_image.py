# Generated by Django 4.1.4 on 2023-02-01 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CategoryApp', '0002_cartmodel_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartmodel',
            name='image',
        ),
    ]
