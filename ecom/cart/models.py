from datetime import timezone
from django.db import models
from user.models import CustomUser,Product,ProductSize
from django.utils import timezone
# Create your models here.


class Coupon(models.Model):
    
    coupon_code=models.CharField(max_length=20,unique=True)
    description = models.TextField()
    discount_type = models.CharField(max_length=20,)
    discount = models.DecimalField(max_digits=5, decimal_places=2)  
    valid_from=models.DateField()
    valid_to=models.DateField()
    applicable_type = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    min_amount=models.IntegerField()  
     
    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now and self.valid_to >= now


class UserCoupon(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True) 
    coupon_applied=models.ForeignKey(Coupon,on_delete=models.CASCADE,null=True)
    is_applied=models.BooleanField(default=True)


class Cart(models.Model):
    user= models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    products = models.ManyToManyField(Product, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    coupon_applied=models.ForeignKey(Coupon,on_delete=models.CASCADE,null=True)
    
    

    def get_total_price(self):
        return sum(item.get_subtotal() for item in self.cart_items.all())
    
    def get_total_quantity(self):
        return sum(item.quantity for item in self.cart_items.all())
    
    def get_total_offerprice(self):
        return sum(item.get_subtotalprice() for item in self.cart_items.all())
    
    def get_price_difference(self):
        return self.get_total_price() - self.get_total_offerprice()
    
    def get_shipping_charge(self):
        total_amount = self.get_total_price()
        if total_amount > 1000:
            return 0
        else:
            return 200

    

    def coupon_discount(self):
        if self.coupon_applied :
            if self.coupon_applied.discount_type == 'Amount':
                return self.coupon_applied.discount
            elif self.coupon_applied.discount_type == 'Percentage':
                return (self.coupon_applied.discount * self.get_total_price()) / 100
        return 0
           
        
    def get_total(self):        
        return self.get_total_price() + self.get_shipping_charge() - self.get_price_difference() - self.coupon_discount()
    


    def get_total(self):        
        return self.get_total_price() + self.get_shipping_charge() - self.get_price_difference()-self.coupon_discount()
    

class CartItem(models.Model):
    user= models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active=models.BooleanField(default=True)

    def get_subtotal(self):
        return self.product_size.price * self.quantity
    
    def get_subtotalprice(self):
        return self.product_size.offer_price * self.quantity
    

class WishList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(Product, through='WishListItem')

class WishListItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Wallet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def _str_(self):
        return f"{self.user.email}'s Wallet"




