from django.contrib import admin
from .models import *

# Register your models here.
class VendorSignUpAdmin(admin.ModelAdmin):
    list_display=['fname','lname','email','password','contact','gender','address','companyaddress','companyname']
admin.site.register(VendorSignUpModel,VendorSignUpAdmin)

class VendorLoginAdmin(admin.ModelAdmin):
    list_display=['email','password']
admin.site.register(VendorLoginModel,VendorLoginAdmin)

class VendorContactAdmin(admin.ModelAdmin):
    list_display=['name','email','subject','message','created_date']
admin.site.register(VendorContactModel,VendorContactAdmin)