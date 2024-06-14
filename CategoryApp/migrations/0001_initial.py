# Generated by Django 4.1.4 on 2023-01-31 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CartModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.IntegerField()),
                ('productId', models.IntegerField()),
                ('productPrice', models.IntegerField(default='')),
                ('qty', models.IntegerField(default='')),
                ('totalPrice', models.IntegerField(default='')),
                ('orderId', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetailsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.IntegerField()),
                ('fname', models.CharField(max_length=100)),
                ('lname', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('contact', models.BigIntegerField()),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('pincode', models.BigIntegerField()),
                ('subTotal', models.IntegerField()),
                ('gstPercentage', models.IntegerField()),
                ('gstAmount', models.FloatField()),
                ('deliveryCharge', models.IntegerField()),
                ('grantTotal', models.FloatField()),
                ('payment', models.CharField(max_length=20)),
                ('paymentVia', models.CharField(max_length=20)),
                ('transactionId', models.TextField()),
                ('orderDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RatingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SubCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CategoryApp.categorymodel')),
            ],
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('price', models.BigIntegerField(default='')),
                ('description', models.TextField(default='')),
                ('specification', models.TextField(default='')),
                ('image', models.ImageField(default='', upload_to='product/')),
                ('subCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CategoryApp.subcategorymodel')),
            ],
        ),
    ]
