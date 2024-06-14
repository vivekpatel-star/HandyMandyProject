from django.contrib import admin
from .models import *

# Register your models here.
class UserSignUpAdmin(admin.ModelAdmin):
    list_display=['fname','lname','email','password','contact','gender','address']
admin.site.register(UserSignUpModel,UserSignUpAdmin)

class UserLoginAdmin(admin.ModelAdmin):
    list_display=['email','password']
admin.site.register(UserLoginModel,UserLoginAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display=['name','email','subject','message','created_date']
admin.site.register(ContactModel,ContactAdmin)