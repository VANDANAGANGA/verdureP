from django.db import models
from user.models import CustomUser,Product,ProductSize,ProfileAddress
import random
import string
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
class ShortUUIDField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 8)
        kwargs.setdefault('unique', True)
        kwargs.setdefault('editable', False)
        kwargs['primary_key'] = True  # Set as primary key
        super().__init__(*args, **kwargs)

    def generate_uuid(self):
        length = self.max_length
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if not value:
            value = self.generate_uuid()
            setattr(model_instance, self.attname, value)
        return value

class Order(models.Model):
    ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Cancelled', 'Cancelled'),
    ('Confirmed', 'Confirmed'),
    ('Out for Shipping', 'Out for Shipping'),
    ('Out for Delivery', 'Out for Delivery'),
    ('Delivered', 'Delivered'),
    ('Returned', 'Returned'),

   )
    
    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    )
   
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_id = ShortUUIDField()
    name = models.CharField(_('name'), max_length=100)
    phone_number = PhoneNumberField(_('mobile number'), blank=True, null=True)
    house_name=models.CharField(_('name'), max_length=100)
    street = models.CharField(_('street'), max_length=100)
    city = models.CharField(_('city'), max_length=100)
    state = models.CharField(_('state'), max_length=100)
    country = models.CharField(_('country'), max_length=100)
    postal_code = models.CharField(_('postal code'), max_length=10)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS)
    payment_method = models.CharField(max_length=50)
    delivery_date = models.DateTimeField(null=True, blank=True)
    total_mrp = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    coupon_discount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)


class OrderItems(models.Model):
    ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Out for Shipping', 'Out for Shipping'),
    ('Confirmed','Confirmed'),
    ('Cancelled','Cancelled'),
    ('Out for Delivery', 'Out for Delivery'),
    ('Delivered', 'Delivered'),
    ('Returned', 'Returned'),
   )
    order_no = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    product_name=models.CharField(_('name'),max_length=30,blank=True)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    delivery_date = models.DateTimeField(null=True, blank=True)
    size = models.CharField(max_length=50)
    product_price = models.DecimalField(max_digits=8, decimal_places=2)
    product_offer_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity= models.IntegerField(null=False)
    amount=models.IntegerField(null=False)
    product_photo = models.ImageField(upload_to='images/')
    return_problem = models.TextField(blank=True, null=True)


