# Generated by Django 4.1.4 on 2023-02-09 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CategoryApp', '0006_ratingmodel_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratingmodel',
            name='productId',
            field=models.IntegerField(default=0),
        ),
    ]