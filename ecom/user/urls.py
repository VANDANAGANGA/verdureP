from django.urls import path
from . import views

urlpatterns = [
    path('',views.welcome,name='welcome'),
    path('about',views.about,name='about'),
    path('getintouch',views.getintouch,name='getintouch'),
    path('sendmessage',views.sendmessage,name='sendmessage'),
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('forgot',views.forgot,name='forgot'),
    path('home',views.home,name='home'),
    path('usersignout',views.usersignout,name='usersignout'),
    path('sendotp',views.sendotp,name='sendotp'),
    path('otplogin',views.otplogin,name='otplogin'),
    path('passwordreset',views.passwordreset,name='passwordreset'),
    path('productdisplay/<int:id>',views.productdisplay,name='productdisplay'),
    path('productdetails/<int:id>/',views.productdetails,name='productdetails'),
    path('productlist',views.productlist,name='productlist'),
    path('searchproduct',views.searchproduct,name='searchproduct'),
    path('searchpriceproduct',views.searchpriceproduct,name='searchpriceproduct'),
    path('userprofile',views.userprofile,name='userprofile'),
    path('add_address',views.add_address,name='add_address'),
    path('add_photo',views.add_photo,name='add_photo'),
    path('delete_address/<int:id>',views.delete_address,name='delete_address'),

    path('email',views.email,name='email'),
    path('emailotp',views.emailotp,name='emailotp'),
    path('enter_otp',views.enter_otp,name='enter_otp'),







    
    
    
    
]