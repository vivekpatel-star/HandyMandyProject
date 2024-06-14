from django.shortcuts import render,redirect
from .models import *
from CategoryApp .models import *
import re
import random
from django.core.mail import send_mail
from django.template import loader

# Create your views here.

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"

def sessionDataView(request):
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
        userDataDict = {'userId':id,'userType':userType,'userFirstName':fname,'userLastName':lname,'userAddress':address,'userGender':gender,'userEmail':email,'userPassword':password,'userContact':contact}
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

def indexview(request):
    sessionData = sessionDataView(request)
    categoryData = CategoryModel.objects.all()
    return render(request,'index.html',{"catData":categoryData,'navData':sessionData})

def aboutview(request):
    sessionData = sessionDataView(request)
    return render(request,'about.html',{'navData':sessionData})   

def userloginview(request):
    sessionData = sessionDataView(request)
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        logindata=UserSignUpModel.objects.filter(email=email) & UserSignUpModel.objects.filter(password=password)
        
        if len(logindata) > 0: 
            request.session['sessionType'] = 'User'
            request.session['sessionId'] = logindata[0].pk
            request.session['sessionFirstName'] = logindata[0].fname
            request.session['sessionLastName'] = logindata[0].lname
            request.session['sessionGender'] = logindata[0].gender
            request.session['sessionAddress'] = logindata[0].address
            request.session['sessionContact'] = logindata[0].contact
            request.session['sessionEmail'] = logindata[0].email
            request.session['sessionPassword'] = logindata[0].password
            return redirect('indexurl')
        else:
            #print("Invalid Credential")
            return render(request,'LOGIN USER.html',{"PasswordError":"Invalid Emailid/Password",'navData':sessionData})
        print("Login Data : ",loginData)
    return render(request,'LOGIN USER.html',{'navData':sessionData})

def userregisterview(request):
    if request.method=="POST":
        print("Form Submit Method Call")
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        password=request.POST['password']
        confirmpassword=request.POST['confirmpassword']
        contact=request.POST['contact']
        gender=request.POST['gender']
        address=request.POST['address']

        if re.match(password_pattern,password):
            if password==confirmpassword:
                checkData = UserSignUpModel.objects.filter(email=email) | UserSignUpModel.objects.filter(contact=contact)
                if len(checkData)>0:
                    return render(request,'USER REGISTER.html',{'RegisterError':"User Already Exists"})
                else:
                    SModel=UserSignUpModel()
                    SModel.fname=fname
                    SModel.lname=lname
                    SModel.email=email
                    SModel.password=password
                    SModel.contact=contact
                    SModel.gender=gender
                    SModel.address=address
                    SModel.save()
                    return redirect('userloginurl')
            else:
                return render(request,'USER REGISTER.html',{'PasswordError':"Confirm Password does not Match",'RegisterError':"User Already Exits"})    
        else:
            return render(request,'USER REGISTER.html',{'PasswordError':'Need Strong Password'})

    return render(request,'USER REGISTER.html')

def userprofileview(request):
    sessionData = sessionDataView(request)

    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        password=request.POST['password']
        contact=request.POST['contact']
        gender=request.POST['gender']
        address=request.POST['address']

        #profileData = UserSignUpModel.objects.get(pk=request.session['sessionId'])

        if re.match(password_pattern,password):
            sModel = UserSignUpModel(pk=request.session['sessionId'])
            sModel.fname = fname
            sModel.lname = lname
            sModel.password = password
            sModel.gender = gender
            sModel.address = address
            sModel.email = email
            sModel.contact = contact
            sModel.password = password
            sModel.save()

            request.session['sessionFirstName'] = fname
            request.session['sessionLastName'] = lname
            request.session['sessionEmail'] = email
            request.session['sessionContact'] = contact
            request.session['sessionPassword'] = password
            request.session['sessionAddress'] = address
            request.session['sessionGender'] = gender

            sessionData = sessionDataView(request)
            return render(request,'user-profile.html',{'navData':sessionData,'successMessage':'Profile Update Successfully'})    
        else:
            return render(request,'user-profile.html',{'navData':sessionData,'successMessage':'Need Strong Password'})
    return render(request,'user-profile.html',{'navData':sessionData})
    

def userlogoutview(request):
    request.session.clear()
    return redirect('indexurl')

def contactview(request):
    sessionData = sessionDataView(request)

    if request.method=="POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        if(re.fullmatch(regex,email)):
            cModel = ContactModel()
            cModel.name = name
            cModel.email = email
            cModel.subject = subject
            cModel.message = message
            cModel.save()
            return render(request,'contact.html',{'navData':sessionData,'successMessage':"Your Query Submitted Successfully"})
        else:
            return render(request,'contact.html',{'navData':sessionData,'successMessage':"Invalid Email Id"})
    return render(request,'contact.html',{'navData':sessionData})

def userforgotpasswordrview(request):
    sessionData = sessionDataView(request)

    if request.method == "POST":

        if request.POST['type'] == "SendOTP":
            email = request.POST['email']
            checkEmailQuery = UserSignUpModel.objects.filter(email=email)
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
                return render(request,'forgot-password.html',{'navData':sessionData,"email":email,"OTP":otp})
            else:
                return render(request,'forgot-password.html',{'navData':sessionData,"ErrorMessage":"Invalid Email Id"})
        elif request.POST['type'] == "Submit":
            email = request.POST['email']
            userotp = request.POST['otp']
            generatedOTP = request.POST['generatedOTP']
            
            if userotp == generatedOTP:
                return render(request,'forgot-password.html',{'navData':sessionData,"email":email,"PASSWORD":"yes"})            
            else:
                return render(request,'forgot-password.html',{'navData':sessionData,"email":email,"OTP":userotp,"OTPError":"Invalid OTP"})
        elif request.POST['type'] == "Password":
            email = request.POST['email']
            new_password = request.POST['new_password']
            confirm_new_passsword = request.POST['confirm_new_password']

            if new_password == confirm_new_passsword:
                checkEmailQuery = UserSignUpModel.objects.get(email=email)
        
                sModel = UserSignUpModel(pk = checkEmailQuery.pk)
                sModel.fname = checkEmailQuery.fname
                sModel.lname = checkEmailQuery.lname
                sModel.password = new_password
                sModel.gender = checkEmailQuery.gender
                sModel.address = checkEmailQuery.address
                sModel.email = checkEmailQuery.email
                sModel.contact = checkEmailQuery.contact
                sModel.save()                
                return redirect('userloginurl')
            else:
                return render(request,'forgot-password.html',{'navData':sessionData,"email":email,"PASSWORD":"yes","PasswordError":"Password Does Not Match"})
        

    return render(request,'forgot-password.html',{'navData':sessionData})        