from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('index/',indexview ,name='indexurl'),
    path('about/',aboutview ,name='abouturl'),
    path('userlogin/',userloginview ,name='userloginurl'),
    path('userregister/',userregisterview ,name='userregisterurl'),
    path('userprofile/',userprofileview ,name='userprofileurl'),
    path('logout/',userlogoutview,name='userlogouturl'),
    path('contact/',contactview ,name='contacturl'),
    path('userforgotpassword/',userforgotpasswordrview ,name='userforgotpdurl'),
]
