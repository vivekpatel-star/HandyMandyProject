from django.db import models
from VendorApp.models import *

# Create your models here.

class CategoryModel(models.Model):
    name = models.CharField(max_length=100,default='')
    
    def __str__(self):
        return self.name

class SubCategoryModel(models.Model):
    category = models.ForeignKey(CategoryModel,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        
class ProductModel(models.Model):
    vendorId = models.IntegerField(default=1)
    subCategory = models.ForeignKey(SubCategoryModel,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,default='')
    price = models.BigIntegerField(default='')
    stock = models.IntegerField(default=0)
    description = models.TextField(default='')
    specification = models.TextField(default='')
    image = models.ImageField(upload_to='product/',default='')

    def __str__(self):
        return self.name

class CartModel(models.Model):
    userId = models.IntegerField()
    vendorId = models.IntegerField(default=1)
    productId = models.IntegerField()
    productPrice = models.IntegerField(default='')
    qty = models.IntegerField(default='')
    totalPrice = models.IntegerField(default='')
    orderId = models.IntegerField()

    def __str__(self):
        return str(self.pk)    

class RatingModel(models.Model):
    userId = models.IntegerField()
    productId = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    review = models.TextField(default='')
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.userId)

class OrderDetailsModel(models.Model):
    userId = models.IntegerField()
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100,)
    email = models.CharField(max_length=100)
    contact = models.BigIntegerField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.BigIntegerField()
    subTotal = models.IntegerField()
    gstPercentage = models.IntegerField()
    gstAmount = models.FloatField()
    deliveryCharge = models.IntegerField()
    grantTotal = models.FloatField()
    payment = models.CharField(max_length=20)
    paymentVia = models.CharField(max_length=20)
    transactionId = models.TextField()
    orderStatus = models.CharField(default='Order Created',max_length=50)
    orderDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)
    
class orderStatusTracking(models.Model):
    orderId = models.CharField(max_length=10)
    deliveryDays = models.IntegerField()
    trackingMessage = models.TextField()

    def __str__(self) -> str:
        return self.orderId
