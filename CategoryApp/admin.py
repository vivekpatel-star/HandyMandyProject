from django.contrib import admin
from .models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display=['name']
admin.site.register(CategoryModel,CategoryAdmin)

class SubcategoryAdmin(admin.ModelAdmin):
    list_display=['category','name']
admin.site.register(SubCategoryModel,SubcategoryAdmin)    

class ProductAdmin(admin.ModelAdmin):
    list_display = ['vendorId','subCategory','name','price','image','description','specification']
admin.site.register(ProductModel,ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ['userId','vendorId','productId','productPrice','qty','totalPrice','orderId']
admin.site.register(CartModel,CartAdmin)

class OrderAdmin(admin.ModelAdmin):
     list_display = ['pk','fname','lname','contact','city','grantTotal','payment','paymentVia','orderDate']
admin.site.register(OrderDetailsModel,OrderAdmin)

class RatingAdmin(admin.ModelAdmin):
     list_display = ['pk','userId','productId','rating','review','created_date']
admin.site.register(RatingModel,RatingAdmin)

class OrderTrackingAdmin(admin.ModelAdmin):
     list_display = ['pk','orderId','deliveryDays','trackingMessage']
admin.site.register(orderStatusTracking,OrderTrackingAdmin)