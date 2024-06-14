from django.shortcuts import render,redirect
from .models import *
import re
import random
from django.core.mail import send_mail
from django.template import loader
from CategoryApp.models import *
from django.conf import settings
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
import json
import pdfkit
import os
from UserApp.models import *

# Create your views here.

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"

def VendorSessionDataView(request):
    userDataDict = {}
    if request.session.has_key('sessionId'):
        id = request.session['sessionId']
        userType = request.session['sessionType']
        fname = request.session['sessionFirstName']
        lname = request.session['sessionLastName']
        email = request.session['sessionEmail']
        password = request.session['sessionPassword']
        address = request.session['sessionAddress']
        gender = request.session['sessionGender']
        contact = request.session['sessionContact']
        companyname=request.session['sessioncompanyname']
        companyaddress=request.session['sessioncompanyaddress']

        userDataDict = {'userId':id,'userType':userType,'userFirstName':fname,'userLastName':lname,'userAddress':address,'userGender':gender,'userEmail':email,'userPassword':password,'userContact':contact,'usercompanyname':companyname,'usercompanyaddress':companyaddress}
    else:
        userDataDict = {}

    categoryData = CategoryModel.objects.all()
    categoryArray = []
    for i in categoryData:
        subCategoryData = SubCategoryModel.objects.filter(category=i.pk)
        #print(i.pk,subCategoryData)
        subCategoryDataArray = []
        for j in subCategoryData:
            subCategoryDict = {'subCatId':j.pk,'subCatName':j.name}
            subCategoryDataArray.append(subCategoryDict)
        #print(subCategoryDataArray)
        categoryDict = {'catId':i.pk,'catName':i.name,'subCategoryData':subCategoryDataArray}
        categoryArray.append(categoryDict)
    #print(categoryArray)
    navData = {'userData':userDataDict,'categoryData':categoryArray}
    return navData    

def indexView(request):
    if request.session.has_key('sessionId'):
        sessionData = VendorSessionDataView(request)
        return render(request,'index_vendor.html',{'navData':sessionData})
    else:
        return render(request,'index_vendor.html')

def vendorloginview(request):
    sessionData = VendorSessionDataView(request)
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        logindata=VendorSignUpModel.objects.filter(email=email) & VendorSignUpModel.objects.filter(password=password)
        
        if len(logindata) > 0: 
            request.session['sessionType'] = 'Vendor'
            request.session['sessionId'] = logindata[0].pk
            request.session['sessionFirstName'] = logindata[0].fname
            request.session['sessionLastName'] = logindata[0].lname
            request.session['sessionGender'] = logindata[0].gender
            request.session['sessionAddress'] = logindata[0].address
            request.session['sessionContact'] = logindata[0].contact
            request.session['sessionEmail'] = logindata[0].email
            request.session['sessionPassword'] = logindata[0].password
            request.session['sessioncompanyname'] = logindata[0].companyname
            request.session['sessioncompanyaddress'] = logindata[0].companyaddress
            return redirect('vendorIndexurl')
        else:
            #print("Invalid Credential")
            return render(request,'LOGIN VENDOR.html',{"PasswordError":"Invalid Emailid/Password",'navData':sessionData})
    return render(request,'LOGIN VENDOR.html',{'navData':sessionData})

def vendorregisterview(request):
    if request.method=="POST":
        print("Form Submit Method Call")
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        password=request.POST['password']
        confirmpassword=request.POST['confirmpassword']
        contact=request.POST['contact']
        gender=request.POST['gender']
        companyname=request.POST['companyname']
        companyaddress=request.POST['companyaddress']
        address=request.POST['address']

        if password==confirmpassword:
            checkData = VendorSignUpModel.objects.filter(email=email) | VendorSignUpModel.objects.filter(contact=contact)
            if len(checkData)>0:
                return render(request,'VENDOR REGISTER.html',{'RegisterError':"User Already Exists"})
            else:
                SModel=VendorSignUpModel()
                SModel.fname=fname
                SModel.lname=lname
                SModel.email=email
                SModel.password=password
                SModel.contact=contact
                SModel.gender=gender
                SModel.address=address
                SModel.companyname=companyname
                SModel.companyaddress=companyaddress
                SModel.save()
                return redirect('vendorloginurl')
        else:
            return render(request,'VENDOR REGISTER.html',{'PasswordError':"Confirm Password does not Match",'RegisterError':"User Already Exits"})

    return render(request,'VENDOR REGISTER.html')

def vendorprofileview(request):
    sessionData = VendorSessionDataView(request)

    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        password=request.POST['password']
        contact=request.POST['contact']
        gender=request.POST['gender']
        address=request.POST['address']
        companyname=request.POST['companyname']
        companyaddress=request.POST['companyaddress']

        profileData = VendorSignUpModel.objects.get(pk=request.session['sessionId'])
        if re.match(password_pattern,password):
            sModel = VendorSignUpModel(pk=request.session['sessionId'])
            sModel.fname = fname
            sModel.lname = lname
            sModel.password = password
            sModel.gender = gender
            sModel.address = address
            sModel.email = email
            sModel.contact = contact
            sModel.password = password
            sModel.companyname = companyname
            sModel.companyaddress = companyaddress
            sModel.save()

            request.session['sessionFirstName'] = fname
            request.session['sessionLastName'] = lname
            request.session['sessionEmail'] = email
            request.session['sessionContact'] = contact
            request.session['sessionPassword'] = password
            request.session['sessionAddress'] = address
            request.session['sessionGender'] = gender
            request.session['sessioncompanyname'] = companyname
            request.session['sessioncompanyaddress'] = companyaddress

            sessionData = VendorSessionDataView(request)
            return render(request,'vendor-profile.html',{'navData':sessionData,'successMessage':'Profile Update Successfully'})    
        else:
            return render(request,'vendor-profile.html',{'navData':sessionData,'successMessage':'Need Strong Password'})
    return render(request,'vendor-profile.html',{'navData':sessionData})


def vendorcontactview(request):
    sessionData = VendorSessionDataView(request)

    if request.method=="POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        cModel = VendorContactModel()
        cModel.name = name
        cModel.email = email
        cModel.subject = subject
        cModel.message = message
        cModel.save()
        return render(request,'vendor-contact.html',{'navData':sessionData,'successMessage':"Your Query Submitted Successfully"})
    return render(request,'vendor-contact.html',{'navData':sessionData})

def vendorforgotpdview(request):
    sessionData = VendorSessionDataView(request)

    if request.method == "POST":

        if request.POST['type'] == "SendOTP":
            email = request.POST['email']
            checkEmailQuery = VendorSignUpModel.objects.filter(email=email)
            if len(checkEmailQuery) >0:
                #Send OTP Code
                otp = random.randrange(1111,9999,4)
                print(otp)
                # html_message = loader.render_to_string(
                #     'email_sender_app/message.html',
                #     {
                #         # TODO: Enter the recipient name
                #         'name': 'Recipient Name',
                #         # TODO:  Update with your own body
                #         'body': 'This email is to verify whether we can send email in Django from Gmail account.',
                #         # TODO: Update the signature
                #         'sign': 'Sender',
                #     })
                send_mail(
                    'RESET Password OTP',
                    'Your verification Code Is : '+str(otp),
                    'vishwamistry18@gmail.com',  # TODO: Update this with your mail id
                    [email],  # TODO: Update this with the recipients mail id
                    fail_silently=False,
                )
                return render(request,'vendor-forgot-password.html',{'navData':sessionData,"email":email,"OTP":otp})
            else:
                return render(request,'vendor-forgot-password.html',{'navData':sessionData,"ErrorMessage":"Invalid Email Id"})
        elif request.POST['type'] == "Submit":
            email = request.POST['email']
            userotp = request.POST['otp']
            generatedOTP = request.POST['generatedOTP']
            
            if userotp == generatedOTP:
                return render(request,'vendor-forgot-password.html',{'navData':sessionData,"email":email,"PASSWORD":"yes"})            
            else:
                return render(request,'vendor-forgot-password.html',{'navData':sessionData,"email":email,"OTP":userotp,"OTPError":"Invalid OTP"})
        elif request.POST['type'] == "Password":
            email = request.POST['email']
            new_password = request.POST['new_password']
            confirm_new_passsword = request.POST['confirm_new_password']

            if new_password == confirm_new_passsword:
                checkEmailQuery = VendorSignUpModel.objects.get(email=email)
        
                sModel = VendorSignUpModel(pk = checkEmailQuery.pk)
                sModel.fname = checkEmailQuery.fname
                sModel.lname = checkEmailQuery.lname
                sModel.email = checkEmailQuery.email
                sModel.password = new_password
                sModel.contact = checkEmailQuery.contact
                sModel.gender = checkEmailQuery.gender
                sModel.address = checkEmailQuery.address
                sModel.companyname = checkEmailQuery.companyname
                sModel.companyaddress = checkEmailQuery.companyaddress
                sModel.save()                
                return redirect('vendorloginurl')
            else:
                return render(request,'vendor-forgot-password.html',{'navData':sessionData,"email":email,"PASSWORD":"yes","PasswordError":"Password Does Not Match"})
    return render(request,'vendor-forgot-password.html',{'navData':sessionData})        
    

def vendorlogoutview(request):
    request.session.clear()
    return redirect('vendorloginurl')

def shopview(request,subCatId):
    # if subCatId==0:
    #     productData = VendorProductModel.objects.all()
    # else:
    #     productData = VendorProductModel.objects.filter(subCategory=subCatId)
    # sessionData = VendorSessionDataView(request)
    # return render(request,'vendorshop.html',{'navData':sessionData,'productData':productData}) 
    if subCatId==0:
        productData = ProductModel.objects.filter(vendorId=request.session['sessionId'])
    else:
        productData = ProductModel.objects.filter(subCategory=subCatId) & ProductModel.objects.filter(vendorId=request.session['sessionId'])

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
        
        print(i.pk,i.name,rating)

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

    sessionData = VendorSessionDataView(request)
    return render(request,'vendorshop.html',{'navData':sessionData,'productData':productArray})

def vendororderview(request):
    sessionData = VendorSessionDataView(request)
    orderData = OrderDetailsModel.objects.all()
    orderDataArray = []
    for i in orderData:
        cartDataArray = []
        cartQuery = CartModel.objects.filter(orderId=i.pk) & CartModel.objects.filter(vendorId=request.session['sessionId'])
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
        if len(cartQuery)>0:
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
        statusType = request.POST['type']
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
        
        if statusType=='accept':
            send_mail(
                    'Your Order (Order Id : '+oModel.pk+" ) Dispatch",
                    'Your Order (Order Id : '+oModel.pk+" ) Dispatch From Our Warehouse.",
                    'vishwamistry18@gmail.com',  # TODO: Update this with your mail id
                    [oDetailModel.email],  # TODO: Update this with the recipients mail id
                    fail_silently=False,
                )
            oModel.orderStatus = "Dispatch"
        else :
            send_mail(
                    'Your Order (Order Id : '+oModel.pk+" ) Rejected",
                    'Your Order (Order Id : '+oModel.pk+" ) Rejected By Our Vendor.",
                    'vishwamistry18@gmail.com',  # TODO: Update this with your mail id
                    [oDetailModel.email],  # TODO: Update this with the recipients mail id
                    fail_silently=False,
                )
            oModel.orderStatus = "Rejected"
        oModel.save()
    
        orderData = OrderDetailsModel.objects.filter(userId=request.session['sessionId'])
        orderDataArray = []
        for i in orderData:
            cartDataArray = []
            cartQuery = CartModel.objects.filter(orderId=i.pk) & CartModel.objects.filter(vendorId=request.session['sessionId'])
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
        return render(request,'vendor-orderpage.html',{'navData':sessionData,'orderData':orderDataArray})   
    return render(request,'vendor-orderpage.html',{'navData':sessionData,'orderData':orderDataArray}) 

def vendorproductdetailview(request,productId):
    sessionData = VendorSessionDataView(request)
    productData = ProductModel.objects.get(pk=productId)
    return render(request,'vendor-product-detail.html',{'productData':productData,'navData':sessionData})  

def vendoraddproductview(request):
    if request.session.has_key('sessionId'):
        sessionData = VendorSessionDataView(request)
        subCatData = SubCategoryModel.objects.all()
        if request.method == "POST" and request.FILES['image']:
            name = request.POST['name']
            subcategory = SubCategoryModel.objects.get(id= request.POST['subCategory'])
            price = request.POST['price']
            stock = request.POST['stock']
            description = request.POST['description']
            specification = request.POST['specification']
            image = request.FILES['image']
            productModel = ProductModel()
            productModel.subCategory = subcategory
            productModel.vendorId = request.session['sessionId']
            productModel.name = name
            productModel.price = price
            productModel.stock = stock
            productModel.description = description
            productModel.specification = specification
            productModel.image = image
            productModel.save()
            return redirect('vendorIndexurl')    
        return render(request,'addproduct.html',{'navData':sessionData,'subCatData':subCatData})
    else:
        return redirect('vendorloginurl')
        

def vendororderstatusview(request,orderId):
    sessionData = VendorSessionDataView(request)
    if request.method == "POST":
        oId = request.POST['orderno']
        days = request.POST['days']
        remark = request.POST['remark']

        orderStatus = orderStatusTracking()
        orderStatus.orderId = oId
        orderStatus.deliveryDays = days
        orderStatus.trackingMessage = remark
        orderStatus.save()
        return redirect('vendororderurl')
    return render(request,'orderstatus.html',{'navData':sessionData,'orderId':orderId})

def vendororderstatuseditview(request,statusId):

    orderStatusData = orderStatusTracking.objects.get(id=statusId)

    sessionData = VendorSessionDataView(request)
    if request.method == "POST":
        oId = request.POST['orderno']
        days = request.POST['days']
        remark = request.POST['remark']

        orderStatus = orderStatusTracking()
        orderStatus.pk = orderStatusData.pk
        orderStatus.orderId = oId
        orderStatus.deliveryDays = days
        orderStatus.trackingMessage = remark
        orderStatus.save()
        return redirect('vendororderurl')
    return render(request,'orderstatus_edit.html',{'navData':sessionData,'orderStatusData':orderStatusData})

def invoiveview(request,orderId):
    sessionData = VendorSessionDataView(request)
    orderData = OrderDetailsModel.objects.get(pk=orderId)
    i = orderData
    cartDataArray = []
    cartQuery = CartModel.objects.filter(orderId=i.pk) & CartModel.objects.filter(vendorId=request.session['sessionId'])
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

    # if request.method == 'POST':
    #     #pdfkit.from_file('invoice.html', 'out.pdf')

    #     #The name of your PDF file
    #     filename = '{}.pdf'.format("1")

    #     #HTML FIle to be converted to PDF - inside your Django directory
    #     template = get_template('invoice.html')

    #     context = {}

    #     #Render the HTML
    #     html = template.render(context)

    #     #Options - Very Important [Don't forget this]
    #     options = {
    #         'encoding': 'UTF-8',
    #         'javascript-delay':'1000', #Optional
    #         'enable-local-file-access': None, #To be able to access CSS
    #         'page-size': 'A4',
    #         'custom-header' : [
    #             ('Accept-Encoding', 'gzip')
    #         ],
    #     }
    #     #Javascript delay is optional

    #     #Remember that location to wkhtmltopdf
    #     config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

    #     #Saving the File
    #     filepath = os.path.join(settings.MEDIA_ROOT, 'client_invoices')
    #     os.makedirs(filepath, exist_ok=True)
    #     pdf_save_path = filepath+filename
    #     #Save the PDF
    #     pdfkit.from_string(html, pdf_save_path, configuration=config, options=options)

        # return render(request,'vendor_invoice.html',{'navData':sessionData,'orderData':orderDataDict})        
    return render(request,'vendor_invoice.html',{'navData':sessionData,'orderData':orderDataDict})    


def userorderAllview(request):
    sessionData = VendorSessionDataView(request)
    userAllData = UserSignUpModel.objects.all()
    userDictArray = []
    userAllDataDict = {}
    for i in userAllData:
        orderData = OrderDetailsModel.objects.all().filter(userId=i.pk)
        orderUserData = []
        for j in orderData:
            cartData = CartModel.objects.all().filter(orderId=j.pk) & CartModel.objects.all().filter(vendorId=request.session['sessionId'])
            if len(cartData) > 0:
                orderUserData.append(j)
            
        if len(orderUserData)>0:
            userAllDataDict = {"firstName":i.fname,"lastName":i.lname,"orderCount":len(orderUserData)}
            userDictArray.append(userAllDataDict)
    return render(request,'vendor-userorder.html',{'navData':sessionData,'orderData':userDictArray})    

def productorderAllview(request):
    sessionData = VendorSessionDataView(request)
    productAllData = ProductModel.objects.filter(vendorId=request.session['sessionId'])
    productDictArray = []
    productAllDataDict = {}
    for i in productAllData:    
        cartData = CartModel.objects.all().filter(productId=i.pk) & CartModel.objects.all().filter(vendorId=request.session['sessionId'])
        cartArray = []
        for j in cartData:
            if j.orderId != 0 :
                cartArray.append(j)
        productAllDataDict = {"productName":i.name,"orderCount":len(cartArray)}
        productDictArray.append(productAllDataDict)
    return render(request,'vendor-productorder.html',{'navData':sessionData,'orderData':productDictArray})    