from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
from .models import CustomUser,Product,ProductSize,Category,ProfileAddress,ProfilePhoto
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.db.models import Q
import random
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password


# Create your views here.
def welcome(request):
    return render(request,'user/index.html')
def about(request):
    return render(request,'user/about.html')
def getintouch(request):
     return render(request,'user/getintouch.html')

def sendmessage(request):
     if request.method == 'POST':
        # Get form data
        name = request.POST.get('contact-name')
        email = request.POST.get('contact-email')
        subject = request.POST.get('contact-subject')
        message = request.POST.get('message')
        print(name,111111111111111111111111111)
        print(email,5555555555555555555555555555555)
        print(subject,88888888888888888888888)
        print(message,7777777777777777777)
        if message is not None:
            email_body = "Hello, my self " + name + ".\n\n" + message
        send_mail(
                subject,
                email_body,
                email,
                ["vandu.ganga96@gmail.com"],
                fail_silently=False,
            )
        messages.success(request,'One time password send to yor email')
        return redirect('about')


def signup(request):
    if request.method == 'POST':
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['email']
        phonenumber = request.POST['phonenumber']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "The email id already exists.")
            return redirect('signup') 
        else:
            my_user = CustomUser.objects.create_user(email=email, password=pass1, first_name=fname, last_name=lname, mobile=phonenumber)
            my_user.save()
            return redirect('signin')

    return render(request, 'user/signup.html')

@never_cache   
def signin(request):
    if request.user.is_authenticated:
        return redirect("productdisplay")
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(request,email=email,password=password)
        if user is not None and user.is_active==True:
           login(request,user)
           return redirect("productlist")
        else:
           messages.warning(request, "Email or password is incorrect!!!")
    return render(request,'user/signin.html')    

@never_cache
def home(request):
    return render(request,'user/shop-details.html')

@never_cache
def usersignout(request):
    logout(request)
    return redirect('welcome')

def forgot(request):
    return render(request,'user/sendotp.html')


def sendotp(request):
    mobile = request.POST.get('mobile')
    print(mobile)
    user_number=CustomUser.objects.filter(mobile=mobile)
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)]) 
    if user_number.exists():
            user=user_number.first()
            user.otp=otp
            user.save()
            request.session['mobile']=request.POST['mobile']  # Replace with your OTP generation logic

    # Add your Twilio account credentials
            account_sid = 'AC4fbd0b570563fad216480c34653c36bc'
            auth_token = 'd9d88ff67b7b8c89476f85fb02dc774e'
    # twilio_number = '+18306943453'

            client = Client(account_sid, auth_token)
            message = client.messages.create(
              body=' welcome to verdure Your OTP is: ' + otp,
              from_='+18306943453',
              to=mobile
            )
            return render(request,'user\otplogin.html')
    else:
        messages.warning(request,"No user registered with the provided mobile number")
        return redirect('forgot')




def otplogin(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        mobile = request.session.get('mobile')

        user_number = CustomUser.objects.filter(mobile=mobile)
        if user_number.exists():
            user = user_number.first()
            if entered_otp == user.otp:
                # OTP verification successful
                user.is_otp_verified = True
                user.save()
                del request.session['mobile']
                login(request, user)
                return redirect('productlist')
            else:
               messages.error(request, 'Invalid OTP')
               return render(request, 'user/otplogin.html')

    return redirect('sendotp')  # Redirect to the OTP sending page if accessed directly without submitting the form

def email(request):
    return render(request,'user/passwordchange.html')

def emailotp(request):
    error_message =None
    otp = random.randint(11111,99999)
    email = request.POST.get('email')
    user_email = CustomUser.objects.filter(email=email)
    if user_email:
        user = CustomUser.objects.get(email = email)
        user.otp =otp
        user.save()
        request.session['email'] = request.POST['email']
        send_mail(
            "welcome to verdure",
            "Your one time otp is"+str(otp),
            "vandu.ganga96@gmail.com",
            [email],
            fail_silently=False,
        )
        messages.success(request,'One time password send to yor email')
        return redirect('enter_otp')
    else:
        error_message ="Invaild email please enter correct email"
        return render(request,'user/forgot.html',{'error':error_message})

def enter_otp(request):
    error_message =None
    if request.session['email']:
        email = request.session['email']
        user = CustomUser.objects.filter(email=email)
        for u in user:
            user_otp = u.otp
        if request.method=="POST":
            otp =request.POST.get('otp')
            if not otp:
                error_message= "otp is required"
            elif not user_otp == otp:
                error_message ="otp is invalid"
            if not error_message:
                return render( request,'user/passwordreset.html')
        return render(request,'user/enter_otp.html')
    else:
        return render(request,"forgot.html")

def passwordreset(request):
    email = request.session.get('email')
    if email:
        user=CustomUser.objects.filter(email=email).first()

        if request.method=='POST':
            pass1=request.POST.get('password1')
            pass2=request.POST.get('password2')
            if pass1!=pass2:
                messages.error(request,'password and confirm password are not same')
            print(pass1)
            user.set_password(pass1)
            user.save()  
            del request.session['email']
            return redirect('signin')
    return render(request,'user\passwordreset.html')


def productdisplay(request,id):
    all_category=Category.objects.all()
    category=Category.objects.get(pk=id)
    product=Product.objects.filter(category=category,is_deleted=False)
    paginator = Paginator(product, per_page=4)  # Display 4 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context={
         'products':product,
         'category': all_category,
         'categories':category,
         'page_obj': page_obj,
    }

     
    return render(request,'user/shop.html',context)



@never_cache
def productlist(request):
    category=Category.objects.all()
    product=Product.objects.filter(is_deleted=False)
    paginator = Paginator(product, per_page=4)  # Display 4 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
         'products':product,
         'category':category,
         'page_obj': page_obj,
    }

    return render(request,'user/shop.html',context)

def productdetails(request,id):
     product = Product.objects.get(pk=id)
    
     print(product)
     size=product.productsize_set.all()
     context={
         'products':product,
         'size':size
     }

     return render(request,'user/shop-details.html',context)


def searchproduct(request):
    if request.method=='POST':
        query=request.POST['query']
        product=Product.objects.filter(Q(product_name__icontains=query))
        print(request,product)
        category=Category.objects.all()
        paginator = Paginator(product, per_page=4)  # Display 4 products per page

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context={
            'products':product,
            'page_obj': page_obj,
            'category':category,
        }
        return render(request,'user/shop.html',context)
    

def searchpriceproduct(request):
    
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        print(min_price)
        print(max_price)
        small_size_products = Product.objects.filter(productsize__size='small')
        if min_price and max_price:
            small_size_products = small_size_products.filter(productsize__price__range=(min_price, max_price)).distinct()
            
        print(small_size_products)
        category=Category.objects.all()
        paginator = Paginator(small_size_products, per_page=4)  # Display 4 products per page

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context={
            'products': small_size_products,
            'page_obj': page_obj,
            'category':category,
        }
        return render(request,'user/shop.html',context)
    
def userprofile(request):
    user=request.user
    profile_address=ProfileAddress.objects.filter(user=user)
    try:
        profile_pic = ProfilePhoto.objects.get(user=user)
    except ProfilePhoto.DoesNotExist:
        profile_pic = None
        
    if profile_address.exists():
        profile_address=profile_address.all()
    else:
        profile_address=None

        
    context={
        'user':user,
        'profile_address':profile_address,
        'profile_pic':profile_pic

    }        
    return render(request,'user/profile.html',context)

def add_address(request):
    user=request.user
    if request.method == 'POST':
        username = request.POST.get('name')
        phone_number=request.POST.get('phone')
        house_name = request.POST.get('housename')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pin = request.POST.get('zip')
        Profile_address=ProfileAddress(user=user)
        # Create a new Address object and save it to the database
        Profile_address.name=username
        Profile_address.house_name=house_name
        Profile_address.street=street
        Profile_address.city=city
        Profile_address.state=state
        Profile_address.phone_number=phone_number
        Profile_address.country=country
        Profile_address.postal_code=pin
        Profile_address.save()
        
        return redirect('userprofile')
    return redirect('userprofile')

# def add_photo(request):
#     user = request.user
#     try:
#         profile_pic = ProfilePhoto.objects.get(user=user)
#     except ProfilePhoto.DoesNotExist:
#         # Handle the case when the user doesn't have a profile picture yet
#         profile_pic=ProfilePhoto(user=user)
    
#     if request.method == 'POST':
#         new_profile_pic = request.FILES.get('profile_pic')
#         if new_profile_pic:
#             profile_pic.profile_pic = new_profile_pic
#             print('photo undoo',new_profile_pic)
#             profile_pic.save()
#     return redirect('userprofile')
    
def add_photo(request):
    user = request.user
    try:
        profile_pic = ProfilePhoto.objects.get(user=user)
    except ProfilePhoto.DoesNotExist:
        # Handle the case when the user doesn't have a profile picture yet
        profile_pic = ProfilePhoto(user=user)

    if request.method == 'POST':
        new_profile_pic = request.FILES.get('profile_pic')
        print(new_profile_pic,999999999999999999999999999999999)
        if new_profile_pic:
            profile_pic.profile_pic = new_profile_pic
            profile_pic.save()
            return JsonResponse({'status': 'success'})  # Return a JSON response instead of redirecting

    return render(request, 'profile.html', {'profile_pic': profile_pic})
 
def delete_address(request,id):
    user = request.user
    if id:
        try:
            address_id = id
            profile_address = get_object_or_404(ProfileAddress, id=address_id, user=user)
            profile_address.delete()
        except (ValueError, ProfileAddress.DoesNotExist):
            pass

    return redirect('userprofile')

