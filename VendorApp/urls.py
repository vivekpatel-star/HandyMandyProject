from django.contrib import admin
from django.urls import path,include
from .views import * 

urlpatterns = [

    path('vendorlogin/',vendorloginview ,name='vendorloginurl'),
    path('vendorregister/',vendorregisterview ,name='vendorregisterurl'),
    path('vendorprofile/',vendorprofileview ,name='vendorprofileurl'),
    path('vendorforgotpassword/',vendorforgotpdview ,name='vendorforgotpdurl'),
    path('vendorcontact/',vendorcontactview ,name='vendorcontacturl'),
    path('vendorlogout/',vendorlogoutview ,name='vendorlogouturl'),
    path('vendororder/',vendororderview ,name='vendororderurl'),
    path('vendorshop/<int:subCatId>/',shopview ,name='vendorshopurl'),
    path('vendororderstatus/<int:orderId>/',vendororderstatusview ,name='vendororderstatusurl'),
    path('vendororderstatusedit/<int:statusId>/',vendororderstatuseditview ,name='vendororderstatusediturl'),
    path('vendoraddproduct/',vendoraddproductview ,name='vendoraddproducturl'),
    path('vendorproductdetail/<int:productId>/',vendorproductdetailview ,name='vendorproductdetailurl'),
    path('vendorInvoice/<int:orderId>/',invoiveview,name='vendorInvoiceurl'),
    path('',indexView ,name='vendorIndexurl'),
    path('productReport/',productorderAllview ,name='userproducturl'),
    path('userOrderReport/',userorderAllview ,name='userorderurl'),
]