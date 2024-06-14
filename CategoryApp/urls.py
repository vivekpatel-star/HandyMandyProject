from django.urls import path
from .views import *

urlpatterns = [
    path('category/<int:catId>/',numkeenview ,name='categoryurl'),
    path('shop/<int:subCatId>/',shopview ,name='shopurl'),
    path('shop_filter/<str:subCatId>/<str:start>/<str:end>/',shopFilterview ,name='shopNewurl'),
    path('numkeen/',numkeenview ,name='numkeenurl'),
    path('productdetail/<int:productId>/',userproductdetailview ,name='productdetailurl'),
    path('cart/',cartview,name='carturl'),
    path('checkout/',checkoutview,name='checkouturl'),
    path('razorpayView/',razorpayView,name='razorpayView'),
    path('paymenthandler/', paymenthandler, name='paymenthandler'),
    path('ordersuccess/',ordersuccessview,name='ordersuccessurl'),
    path('order/',myorderview,name='myorderurl'),
    path('invoice/<int:orderId>/',invoiveview,name='invoiceurl'),
    path('removeCart/<int:cartId>/',removeCartView,name='removeCartUrl'),
    path('rating/<int:productId>/',ratingView,name='ratingUrl'),
    path('cart_user_data/',cart_user_data,name='cart_user_data_url'),
    path('pdf/',pdf,name='pdf'),
]