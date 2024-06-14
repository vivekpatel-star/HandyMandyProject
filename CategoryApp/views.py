from django.shortcuts import render,redirect
from UserApp.views import *
from .models import *
import pdfkit
import os
from django.conf import settings
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
import json
import razorpay
from django.http import HttpResponseBadRequest

# Create your views here.

def categoryview(request,catId):
    sessionData = sessionDataView(request)
    subCategoryData = CategoryModel.objects.filter(category=catId)
    return render(request,'shop.html',{'subCatData':subCategoryData,'navData':sessionData})

def SubCategoryView(request,catId):
    sessionData = sessionDataView(request)
    subCategoryData = SubCategoryModel.objects.filter(category=catId)
    return render(request,'shop.html',{'subCatData':subCategoryData,'navData':sessionData})

def userproductdetailview(request,productId):
    sessionData = sessionDataView(request)
    productData = ProductModel.objects.get(pk=productId)
    orderProductDataNew = CartModel.objects.filter(productId=productId)
    iOrderCountNew = 0
    for i in orderProductDataNew:
        if i.orderId != 0:
            iOrderCountNew = iOrderCountNew+ (i.qty)    
    sStockFlag = False
    if productData.stock > iOrderCountNew:
        sStockFlag = True
    if request.method=="POST":
        if request.session.has_key('sessionId'):
            proId = request.POST['proId']
            proPrice = request.POST['proPrice']
            vendorId = request.POST['vendorId']
            qty = 1
            totalPrice = qty * int(proPrice)
            userId = request.session['sessionId']
            orderProductData = CartModel.objects.filter(productId=proId)
            iOrderCount = 0
            for i in orderProductData:
                if i.orderId != 0:
                    iOrderCount = iOrderCount+ (i.qty)
            print("Total Ordered Product",iOrderCount)
            if productData.stock > iOrderCount:
                cartDataCheck = CartModel.objects.filter(userId=userId) & CartModel.objects.filter(productId=proId) & CartModel.objects.filter(orderId=0)
                if len(cartDataCheck) > 0 :
                    return render(request,'user-product-detail.html',{'productData':productData,'navData':sessionData,"isStock":sStockFlag,'errorMessage': 'Product Already Added In Cart'})
                else:
                    cartModel = CartModel()
                    cartModel.userId = userId
                    cartModel.vendorId = vendorId
                    cartModel.productId = proId
                    cartModel.productPrice = proPrice
                    cartModel.qty= qty
                    cartModel.totalPrice = totalPrice
                    cartModel.orderId = 0
                    cartModel.save()
            else:
                return render(request,'user-product-detail.html',{'productData':productData,'navData':sessionData,"isStock":sStockFlag,'errorMessage': 'Product Out Of Stock'})
        else:
            return redirect('userloginurl')
            #return render(request,'user-product-detail.html',{'productData':productData,'navData':sessionData,'errorMessage': 'Please Login And Proceed for Add To Cart'})
    return render(request,'user-product-detail.html',{'productData':productData,'navData':sessionData,"isStock":sStockFlag})    

def shopview(request,subCatId):
    if subCatId==0:
        productData = ProductModel.objects.all()
    else:
        productData = ProductModel.objects.filter(subCategory=subCatId)
    productArray = []
    for i in productData:
        ratingData = RatingModel.objects.filter(productId=i.pk)
        totalUserRating = len(ratingData)
        totalRating = 0
        for j in ratingData:
            totalRating += j.rating
        if totalUserRating==0:
            rating=0
        else:
            rating = totalRating/totalUserRating
        productDict = {
            "pk":i.pk,
            "subCategory":i.subCategory,
            "name":i.name,
            "price":i.price,
            "description":i.description,
            "specification":i.specification,
            "image":i.image,
            "rating" : rating
            }
        productArray.append(productDict)
    sessionData = sessionDataView(request)
    return render(request,'shop.html',{'navData':sessionData,'productData':productArray,'subCat':subCatId})     

def shopFilterview(request,subCatId,start,end):
    iStart = int(start)
    iEnd = int(end)
    if subCatId=="0":        
        productData = ProductModel.objects.all()
    else:
        productData = ProductModel.objects.filter(subCategory=subCatId)
    productArray = []
    for i in productData:
        if i.price > iStart-1:
            if i.price < iEnd+1:
                ratingData = RatingModel.objects.filter(productId=i.pk)
                totalUserRating = len(ratingData)
                totalRating = 0
                for j in ratingData:
                    totalRating += j.rating
                if totalUserRating==0:
                    rating=0
                else:
                    rating = totalRating/totalUserRating
                
                productDict = {
                    "pk":i.pk,
                    "subCategory":i.subCategory,
                    "name":i.name,
                    "price":i.price,
                    "description":i.description,
                    "specification":i.specification,
                    "image":i.image,
                    "rating" : rating
                    }
                productArray.append(productDict)
    sessionData = sessionDataView(request)
    return render(request,'shop.html',{'navData':sessionData,'productData':productArray})     

def numkeenview(request):
    sessionData = sessionDataView(request)
    return render(request,'Numkeen.html',{'navData':sessionData})

def cartview(request):
    sessionData = sessionDataView(request)
    cartQuery = CartModel.objects.filter(userId=request.session['sessionId']) & CartModel.objects.filter(orderId=0)
    cartDataArray = []
    cartTotal = 0
    for i in cartQuery:
        cartTotal += i.totalPrice
        productData = ProductModel.objects.get(pk=i.productId)
        cartDictionary = {
            "cartId": i.pk,
            "vendorId": i.vendorId,
            "productId":i.productId,
            "productName": productData.name,
            "productImage": productData.image,
            "productPrice" : i.productPrice, 
            "qty" : i.qty,
            "totalPrice" : i.totalPrice
            }
        cartDataArray.append(cartDictionary)
    totalProduct = len(cartDataArray)
    gstPercent = 18
    gstAmount = (cartTotal*gstPercent)/100
    deliveryCharge = 20
    finalTotal = cartTotal+gstAmount+deliveryCharge
    request.session['cartTotal'] = cartTotal
    request.session['gstPercentage'] = gstPercent
    request.session['gstAmount'] = gstAmount
    request.session['deliveryCharge'] = deliveryCharge
    request.session['finalTotal'] = finalTotal
    cartDataDict = {
        "cartTotal": cartTotal,
        "gstPercent":gstPercent,
        "gstAmount":gstAmount,
        "deliveryCharge":deliveryCharge,
        "finalTotal" : finalTotal,
        "cartTotalProduct":totalProduct,
        "cartData":cartDataArray}
    return render(request,'cart.html',{'navData':sessionData,'cartDictData':cartDataDict,'totalProduct':totalProduct})

def checkoutview(request):
    sessionData = sessionDataView(request)
    if request.method == 'POST':    
        oModel = OrderDetailsModel()
        oModel.userId = request.session['sessionId']
        oModel.fname = request.POST['fname']
        oModel.lname = request.POST['lname']
        oModel.email = request.POST['email']
        oModel.contact = request.POST['contact']
        oModel.address = request.POST['address']
        oModel.city = request.POST['city']
        oModel.pincode = request.POST['pincode']
        oModel.subTotal = request.session['cartTotal']
        oModel.gstPercentage = request.session['gstPercentage']
        oModel.gstAmount = request.session['gstAmount']
        oModel.deliveryCharge = request.session['deliveryCharge']
        oModel.grantTotal = request.session['finalTotal']
        oModel.payment = request.POST['payment']
        if oModel.payment=="Cash On Delivery":
            oModel.paymentVia = ''
            oModel.transactionId = ''
            oModel.orderStatus = "Order Created"
            oModel.save()
            cartQuery = CartModel.objects.filter(userId=request.session['sessionId']) & CartModel.objects.filter(orderId=0)
            for i in cartQuery:
                cModel = CartModel(pk = i.pk)
                cModel.userId = i.userId
                cModel.vendorId = i.vendorId
                cModel.productId = i.productId
                cModel.productPrice = i.productPrice
                cModel.qty = i.qty
                cModel.totalPrice = i.totalPrice
                cModel.orderId = int(oModel.pk)
                cModel.save()
            return redirect('ordersuccessurl')
        else:
            request.session['shippingUserId']=request.session['sessionId']
            request.session['shippingfname']=request.POST['fname']
            request.session['shippinglname']=request.POST['lname']
            request.session['shippingemail']=request.POST['email']
            request.session['shippingcontact']=request.POST['contact']
            request.session['shippingaddress']=request.POST['address']
            request.session['shippingcity']=request.POST['city']
            request.session['shippingpincode']=request.POST['pincode']
            request.session['shippingsubTotal']=request.session['cartTotal']
            request.session['shippinggstPercentage']=request.session['gstPercentage']
            request.session['shippinggstAmount']=request.session['gstAmount']
            request.session['shippingdeliveryCharge']=request.session['deliveryCharge']
            request.session['shippinggrantTotal']=request.session['finalTotal']
            request.session['shippingpayment']='Online'
            request.session['shippingpaymentVia']='Razorpay'
            request.session['shippingtransactionId']=""
            request.session['shippingorderStatus']="Order Created"
            return redirect('razorpayView')
    return render(request,'checkout.html',{'navData':sessionData})
RAZOR_KEY_ID = 'rzp_test_8iwTTjUECLclBG'
RAZOR_KEY_SECRET = '0q8iXqBL1vonQGVQn4hK1tYg'
client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))

def razorpayView(request):
    currency = 'INR'
    amount = int(request.session['shippinggrantTotal'])*100
    # Create a Razorpay Order
    razorpay_order = client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'http://127.0.0.1:8000/category/paymenthandler/'    
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url    
    return render(request,'razorpayDemo.html',context=context)
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            # verify the payment signature.
            result = client.utility.verify_payment_signature(
                params_dict)
            amount = int(request.session['shippinggrantTotal'])*100  # Rs. 200
            # capture the payemt
            client.payment.capture(payment_id, amount)
            #Order Save Code
            oModel = OrderDetailsModel()
            oModel.userId = request.session['shippingUserId']
            oModel.fname = request.session['shippingfname']
            oModel.lname = request.session['shippinglname']
            oModel.email = request.session['shippingemail']
            oModel.contact = request.session['shippingcontact']
            oModel.address = request.session['shippingaddress']
            oModel.city = request.session['shippingcity']
            oModel.pincode = request.session['shippingpincode']
            oModel.subTotal = request.session['shippingsubTotal']
            oModel.gstPercentage = request.session['shippinggstPercentage']
            oModel.gstAmount = request.session['shippinggstAmount']
            oModel.deliveryCharge = request.session['shippingdeliveryCharge']
            oModel.grantTotal = request.session['shippinggrantTotal']
            oModel.payment = request.session['shippingpayment']
            oModel.paymentVia = request.session['shippingpaymentVia']
            oModel.transactionId = payment_id
            oModel.orderStatus = request.session['shippingorderStatus']
            oModel.save()
            cartQuery = CartModel.objects.filter(userId=request.session['sessionId']) & CartModel.objects.filter(orderId=0)
            for i in cartQuery:
                cModel = CartModel(pk = i.pk)
                cModel.userId = i.userId
                cModel.productId = i.productId
                cModel.productPrice = i.productPrice
                cModel.qty = i.qty
                cModel.totalPrice = i.totalPrice
                cModel.orderId = int(oModel.pk)
                cModel.save()
            return redirect('ordersuccessurl')
        except:
            print("Hello")
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        print("Hello1")
       # if other than POST request is made.
        return HttpResponseBadRequest()

def ordersuccessview(request):
    sessionData = sessionDataView(request)
    return render(request,'ordersuccess.html',{'navData':sessionData})

def myorderview(request):
    sessionData = sessionDataView(request)
    orderData = OrderDetailsModel.objects.filter(userId=request.session['sessionId'])
    orderDataArray = []
    for i in orderData:
        cartDataArray = []
        cartQuery = CartModel.objects.filter(orderId=i.pk)
        for j in cartQuery:        
            productData = ProductModel.objects.get(pk=j.productId)
            cartDictionary = {
                "cartId": j.pk,
                "productId":j.productId,
                "productName": productData.name,
                "productImage": productData.image,
                "productPrice" : j.productPrice, 
                "qty" : j.qty,
                "totalPrice" : j.totalPrice
                }
            cartDataArray.append(cartDictionary)
        orderStatusData = orderStatusTracking.objects.filter(orderId=i.pk)
        if len(orderStatusData)>0 :
            orderStatusDictionary = {
                "statusId": orderStatusData[0].pk,
                "deliveryDays":orderStatusData[0].deliveryDays,
                "trackingMessage": orderStatusData[0].trackingMessage
                }
        else:
            orderStatusDictionary = {}
        orderDataDict = {
            "pk" : i.pk,
            "userId" : i.userId,
            "fname" : i.fname,
            "lname" : i.lname,
            "email" : i.email,
            "contact" : i.contact,
            "address" : i.address,
            "city" : i.city,
            "pincode" : i.pincode,
            "subTotal" : i.subTotal,
            "gstPercentage" : i.gstPercentage,
            "gstAmount" : i.gstAmount,
            "deliveryCharge" : i.deliveryCharge,
            "grantTotal" : i.grantTotal,
            "payment" : i.payment,
            "paymentVia" : i.paymentVia,
            "transactionId" : i.transactionId,
            "orderDate" : i.orderDate,
            "orderStatus" : i.orderStatus,
            "cartData" : cartDataArray,
            "statusData" : orderStatusDictionary
        }
        orderDataArray.append(orderDataDict)
    if request.method == "POST":
        orderId = request.POST['orderId']
        oDetailModel = OrderDetailsModel.objects.get(pk=orderId)
        oModel = OrderDetailsModel(pk=orderId)
        oModel.userId = oDetailModel.userId
        oModel.fname = oDetailModel.fname
        oModel.lname = oDetailModel.lname
        oModel.email = oDetailModel.email
        oModel.contact = oDetailModel.contact
        oModel.address = oDetailModel.address
        oModel.city = oDetailModel.city
        oModel.pincode = oDetailModel.pincode
        oModel.subTotal = oDetailModel.subTotal
        oModel.gstPercentage = oDetailModel.gstPercentage
        oModel.gstAmount = oDetailModel.gstAmount
        oModel.deliveryCharge = oDetailModel.deliveryCharge
        oModel.grantTotal = oDetailModel.grantTotal
        oModel.payment = oDetailModel.payment
        oModel.paymentVia = oDetailModel.paymentVia
        oModel.transactionId = oDetailModel.transactionId
        oModel.orderStatus = "Cancel"
        oModel.save()
        orderData = OrderDetailsModel.objects.filter(userId=request.session['sessionId'])
        orderDataArray = []
        for i in orderData:
            cartDataArray = []
            cartQuery = CartModel.objects.filter(orderId=i.pk)
            for j in cartQuery:        
                productData = ProductModel.objects.get(pk=j.productId)
                cartDictionary = {
                    "cartId": j.pk,
                    "productId":j.productId,
                    "productName": productData.name,
                    "productImage": productData.image,
                    "productPrice" : j.productPrice, 
                    "qty" : j.qty,
                    "totalPrice" : j.totalPrice
                    }
                cartDataArray.append(cartDictionary)
            orderStatusData = orderStatusTracking.objects.filter(orderId=i.pk)
            if len(orderStatusData)>0 :
                orderStatusDictionary = {
                    "statusId": orderStatusData[0].pk,
                    "deliveryDays":orderStatusData[0].deliveryDays,
                    "trackingMessage": orderStatusData[0].trackingMessage
                    }
            else:
                orderStatusDictionary = {}
            orderDataDict = {
                "pk" : i.pk,
                "userId" : i.userId,
                "fname" : i.fname,
                "lname" : i.lname,
                "email" : i.email,
                "contact" : i.contact,
                "address" : i.address,
                "city" : i.city,
                "pincode" : i.pincode,
                "subTotal" : i.subTotal,
                "gstPercentage" : i.gstPercentage,
                "gstAmount" : i.gstAmount,
                "deliveryCharge" : i.deliveryCharge,
                "grantTotal" : i.grantTotal,
                "payment" : i.payment,
                "paymentVia" : i.paymentVia,
                "transactionId" : i.transactionId,
                "orderDate" : i.orderDate,
                "orderStatus" : i.orderStatus,
                "cartData" : cartDataArray,
                "statusData" : orderStatusDictionary
            }
            orderDataArray.append(orderDataDict)
        #orderData = OrderDetailsModel.objects.filter(userId=request.session['sessionId'])
        return render(request,'userorderpage.html',{'navData':sessionData,'orderData':orderDataArray})   
    return render(request,'userorderpage.html',{'navData':sessionData,'orderData':orderDataArray})    

def invoiveview(request,orderId):
    sessionData = sessionDataView(request)
    orderData = OrderDetailsModel.objects.get(pk=orderId)
    i = orderData
    cartDataArray = []
    cartQuery = CartModel.objects.filter(orderId=i.pk)
    for j in cartQuery:        
        productData = ProductModel.objects.get(pk=j.productId)
        cartDictionary = {
            "cartId": j.pk,
            "productId":j.productId,
            "productName": productData.name,
            "productImage": productData.image,
            "productPrice" : j.productPrice, 
            "productDescription" : productData.description,
            "qty" : j.qty,
            "totalPrice" : j.totalPrice
            }
        cartDataArray.append(cartDictionary)
    orderDataDict = {
        "pk" : i.pk,
        "userId" : i.userId,
        "fname" : i.fname,
        "lname" : i.lname,
        "email" : i.email,
        "contact" : i.contact,
        "address" : i.address,
        "city" : i.city,
        "pincode" : i.pincode,
        "subTotal" : i.subTotal,
        "gstPercentage" : i.gstPercentage,
        "gstAmount" : i.gstAmount,
        "deliveryCharge" : i.deliveryCharge,
        "grantTotal" : i.grantTotal,
        "payment" : i.payment,
        "paymentVia" : i.paymentVia,
        "transactionId" : i.transactionId,
        "orderDate" : i.orderDate,
        "orderStatus" : i.orderStatus,
        "cartData" : cartDataArray
    }
    if request.method == 'POST':
        #pdfkit.from_file('invoice.html', 'out.pdf')
        #The name of your PDF file
        filename = '{}.pdf'.format("1")
        #HTML FIle to be converted to PDF - inside your Django directory
        template = get_template('invoice.html')
        context = {}
        #Render the HTML
        html = template.render(context)
        #Options - Very Important [Don't forget this]
        options = {
            'encoding': 'UTF-8',
            'javascript-delay':'1000', #Optional
            'enable-local-file-access': None, #To be able to access CSS
            'page-size': 'A4',
            'custom-header' : [
                ('Accept-Encoding', 'gzip')
            ],
        }
        #Javascript delay is optional
        #Remember that location to wkhtmltopdf
        config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        #Saving the File
        filepath = os.path.join(settings.MEDIA_ROOT, 'client_invoices')
        os.makedirs(filepath, exist_ok=True)
        pdf_save_path = filepath+filename
        #Save the PDF
        pdfkit.from_string(html, pdf_save_path, configuration=config, options=options)
        return render(request,'invoice.html',{'navData':sessionData,'orderData':orderDataDict})        
    return render(request,'invoice.html',{'navData':sessionData,'orderData':orderDataDict})    

def removeCartView(request,cartId):
    cartRemoveData = CartModel.objects.get(pk=cartId)
    cartRemoveData.delete()
    return redirect('carturl')    

def ratingView(request,productId):
    sessionData = sessionDataView(request)
    productData = ProductModel.objects.get(pk=productId)

    if request.method=='POST':
        rating = request.POST['rate']
        review = request.POST['review']

        rateModel = RatingModel()
        rateModel.userId = request.session['sessionId']
        rateModel.productId = productId
        rateModel.rating = rating
        rateModel.review = review
        rateModel.save()
    return render(request,'rating.html',{'navData':sessionData,"productData":productData}) 
    
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@csrf_exempt
def cart_user_data(request):
    x=request.body.decode('utf-8')
    body = json.loads(x)
    cartId = body['cartId']
    proId = body['productId']
    proPrice = body['productPrice']
    qty = body['qty']
    cartType = body['type']
    if request.session.has_key('sessionId'):
        if cartType=="Remove":        
            cartRemoveData = CartModel.objects.get(pk=cartId)
            cartRemoveData.delete()
            return redirect('carturl')
        else:
            cartDataCheck = CartModel.objects.get(pk=cartId)
            cartModel = CartModel()
            cartModel.pk = cartDataCheck.pk
            cartModel.vendorId = cartDataCheck.vendorId
            cartModel.orderId = "0"
            cartModel.productId = cartDataCheck.productId
            cartModel.userId = cartDataCheck.userId
            cartModel.qty = qty
            cartModel.productPrice = cartDataCheck.productPrice
            cartModel.totalPrice = str(int(qty) * int(cartDataCheck.productPrice))
            cartModel.save()
            return redirect('carturl')
    else:
        return redirect('LoginUrl')
#print("Cart View Data ",proId,qty,cartType)
#return redirect('ProductSessionUrl')

import pyautogui
pyautogui.hotkey('ctrl', 'esc')

def pdf(request):
    return pdfkit.from_file('invoice.html', 'out.pdf')