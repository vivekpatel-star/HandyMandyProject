from django.db import models

# Create your models here.
genderchoice=(
    ('male','male'),
    ('female','female'),
)
class VendorSignUpModel(models.Model):
    fname=models.CharField(max_length=20,default='')
    lname=models.CharField(max_length=20,default='')
    email=models.EmailField()
    password=models.CharField(max_length=20,default='')
    contact=models.BigIntegerField()
    gender=models.CharField(max_length=6,default='')
    address=models.CharField(max_length=100,default='')
    companyname=models.CharField(max_length=20,default='')
    companyaddress=models.CharField(max_length=100,default='')

    def __str__(self):
        return self.fname+" "+self.lname

class VendorLoginModel(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=20)

    def __str__(self):
        return self.email     
    
class VendorContactModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name