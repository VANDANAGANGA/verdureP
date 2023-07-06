from django.urls import path
from . import views

app_name = 'cart'


urlpatterns = [
    path('add_to_cart/<int:id>/',views.add_to_cart,name='add_to_cart'),
    path('carts',views.carts,name='carts'),
    path('delete_cart_item/<int:id>/',views.delete_cart_item,name='delete_cart_item'),
    path('update_cart_item/<int:id>/',views.update_cart_item,name='update_cart_item'), 
    path('add_to_wishlist/<int:id>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('wishlistdisplay',views.wishlistdisplay,name='wishlistdisplay'),
    path('remove_from_wishlist/<int:id>/',views.remove_from_wishlist,name='remove_from_wishlist'), 
    path('apply_coupon',views.apply_coupon,name='apply_coupon'), 







    
    

]