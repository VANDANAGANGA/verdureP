from django.urls import path
from . import views

app_name = 'checkout'


urlpatterns = [
    path('checkout',views.checkout,name='checkout'),
    path('order',views.order,name='order'),
    path('razorpay_payment/<int:id>',views.razorpay_payment,name='razorpay_payment'),
    path('userorder',views.userorder,name='userorder'),
    path('cancelorderitem',views.cancelorderitem,name='cancelorderitem'),
    path('returnorderitem',views.returnorderitem,name='returnorderitem'),
    path('returnproduct',views.returnproduct,name='returnproduct'),
    path('cancelorder',views.cancelorder,name='cancelorder'),
    path('order_details/<str:order_id>/', views.order_details, name='order_details'),



]
