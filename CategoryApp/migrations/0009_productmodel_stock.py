# Generated by Django 4.1 on 2023-02-24 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CategoryApp', '0008_orderstatustracking'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='stock',
            field=models.IntegerField(default=0),
        ),
    ]
