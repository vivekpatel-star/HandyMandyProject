from django.db import models
from django.core import validators

# Create your models here.
genderchoice=(
    ('male','male'),
    ('female','female'),
)
class UserSignUpModel(models.Model):
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    email=models.EmailField()
    password=models.CharField(max_length=20)
    contact=models.BigIntegerField()
    gender=models.CharField(max_length=6)
    address=models.CharField(max_length=100)

    def __str__(self):
        return self.email
class UserLoginModel(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=20)

    def __str__(self):
        return self.email     
class ContactModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100,validators=[validators.EmailValidator(message="Invalid Email")])
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name