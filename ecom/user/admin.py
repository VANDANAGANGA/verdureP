from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Product,ProductSize,Category,ProfileAddress,ProfilePhoto

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display=('id','email','password','first_name','last_name','mobile','otp')
admin.site.register(get_user_model(),CustomUserAdmin)


class ProductAdmin(admin.ModelAdmin):
     list_display=('productname','category','description')
admin.site.register(Product)


# class ProductSizeAdmin(admin.ModelAdmin):
#     list_display=['product_id','size','price','offer_price','quantity','product_photo']
admin.site.register(ProductSize)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display=['id','name']
admin.site.register(Category)


admin.site.register(ProfileAddress)
admin.site.register(ProfilePhoto)
