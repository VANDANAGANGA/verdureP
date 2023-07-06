

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=30, blank=True)
    mobile = PhoneNumberField(_('mobile number'), blank=True, null=True)
    otp = models.CharField(_('OTP'), max_length=6, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def _str_(self):
       return self.email

class Category(models.Model):
    category_name=models.CharField(_('name'),max_length=30,blank=True)
    def _str_(self):
       return self.category_name


class Product(models.Model):
    product_name=models.CharField(_('name'),max_length=30,blank=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    description=models.CharField(_('description'),max_length=10000,blank=True)
    image = models.ImageField(upload_to='images/')
    is_deleted = models.BooleanField(default=False)
    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def undo(self):
        self.is_deleted = False
        self.save()
        
    
    def _str_(self):
       return self.product_name



class ProductSize(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    offer_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    product_photo = models.ImageField(upload_to='images/')

    def _str_(self):
        return f"{self.size} - {self.product.name}"

    
class ProfileAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=100)
    phone_number = PhoneNumberField(_('mobile number'), blank=True, null=True)
    house_name=models.CharField(_('name'), max_length=100)
    street = models.CharField(_('street'), max_length=100)
    city = models.CharField(_('city'), max_length=100)
    state = models.CharField(_('state'), max_length=100)
    country = models.CharField(_('country'), max_length=100)
    postal_code = models.CharField(_('postal code'), max_length=10)
    


    def _str_(self):
        return f"{self.user.email}'s Address"

class ProfilePhoto(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(_('profile picture'), upload_to='profile_pics/')


