from django.urls import path
from . import views

urlpatterns = [
    path('',views.adminsignin,name='adminsignin'),
    path('userdisplay',views.userdisplay,name='userdisplay'),
    path('search_user',views.search_user,name='search_user'),
    path('user_block/<int:id>',views.user_block,name='user_block'),
    path('user_unblock/<int:id>',views.user_unblock,name='user_unblock'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('product_display',views.product_display,name='product_display'),
    path('search_product',views.search_product,name='search_product'),
    path('delete_product/<int:id>',views.delete_product,name='delete_product'),
    path('undo_product/<int:id>/', views.undo_product,name='undo_product'),
    path('edit_product/<int:id>',views.edit_product,name='edit_product'),
    path('categorylist',views.categorylist,name='categorylist'),
    path('delete/<int:id>/', views.delete_category,name='delete_category'),
    path('search_category',views.search_category,name='search_category'),
    path('add_category',views.add_category,name='add_category'),
    path('home',views.home,name='home'),
    path('adminsignout',views.adminsignout,name='adminsignout'),
    path('order_display',views.order_display,name='order_display'),
    path('change_orderitem_status',views.change_orderitem_status,name='change_orderitem_status'),
    path('change_order_status',views.change_order_status,name='change_order_status'),
    



    path('coupon',views.coupon,name="coupon"),
    path('add_coupon',views.add_coupon,name="add_coupon"),

    
    path('totalsales',views.totalsales,name='totalsales'),
    path('todaysales',views.todaysales,name='todaysales'),
    path('weeksales',views.weeksales,name='weeksales'),
    path('monthlysales',views.monthlysales,name='monthlysales'),
    path('yearlysales',views.yearlysales,name='yearlysales'),
    path('fromtosales',views.fromtosales,name='fromtosales'),
    path('pdf_generator',views.pdf_generator,name='pdf_generator'),
    
   
    
    
    
]