from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart,CartItem,WishList,WishListItem,Coupon,UserCoupon
from user.models import CustomUser,Product,ProductSize
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone




# Create your views here.
def add_to_cart(request, id):
    product = get_object_or_404(Product, pk=id)
    
    if request.method == 'POST':
        user = request.user if request.user.is_authenticated else None
        cart, _ = Cart.objects.get_or_create(user=user)
        product_size_id = request.POST.get('product_size_id')
        product_size = get_object_or_404(ProductSize, pk=product_size_id)
        quantity = int(request.POST.get('quantity', 1)) 
        cart_item, created = cart.cart_items.get_or_create(product=product, product_size=product_size)
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product_size.quantity:
                cart_item.quantity = product_size.quantity
        else:
            cart_item.quantity = quantity   
        cart_item.save()
    return redirect('cart:carts')

def update_cart_item(request, id):
    user=request.user
    cart_item = get_object_or_404(CartItem, id=id)
    cart=Cart.objects.get(user=user)
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 0))
        if new_quantity >= 0:
            cart_item.quantity = new_quantity
            cart_item.save()

    # Prepare the data to be sent back in the AJAX response
    data = {
        'subtotal': cart_item.get_subtotal(),
        'price':cart.get_total_price(),
        'quantity':cart.get_total_quantity(),
    }

    # Return the updated data as a JSON response
    return JsonResponse(data)

def delete_cart_item(request,id):
    cart_item = get_object_or_404(CartItem, pk=id)
    cart_item.delete()
    return redirect('cart:carts')

def carts(request):
    user = request.user if request.user.is_authenticated else None
    cart=Cart.objects.get(user=user)if user else None
    cart_items =CartItem.objects.filter(cart__user=user)
    context ={
         'cart_items':cart_items,
         'cart':cart
    }
    return render(request,'user/cart.html',context)


def add_to_wishlist(request,id):
   user = request.user 
   if not user.is_authenticated:
        return redirect('signin')
   product = get_object_or_404(Product, id=id)
   wishlist = WishList.objects.filter(user=user).first()
   if not wishlist:
        wishlist = WishList.objects.create(user=user)
   wishlist.products.add(product)
   return redirect('cart:wishlistdisplay')


def wishlistdisplay(request):
    user = request.user if request.user.is_authenticated else None
    wishlist = WishList.objects.filter(user=user).first() if user else None
    wishlist_items = wishlist.wishlist_items.all() if wishlist else []
    context ={
         'wishlist':wishlist,
         'wishlist_items': wishlist_items,
    
    }
    return render(request,'user/wishlist.html',context)

def remove_from_wishlist(request, id):
    user = request.user
    print(user)
    if not user.is_authenticated:
        messages.error(request, 'User must be logged in.')
        return redirect('cart:wishlistdisplay')

    product = get_object_or_404(Product, id=id)
    wishlist = get_object_or_404(WishList, user=request.user)
    wishlist_items = WishListItem.objects.filter(wishlist=wishlist, product=product)
    if wishlist_items.exists():
        wishlist_items.delete()
        messages.success(request, 'Product removed from wishlist.')
    else:
        messages.error(request, 'Product is not in the wishlist.')
    
    return redirect('cart:wishlistdisplay')

def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon-code')
        user = request.user
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
        except Coupon.DoesNotExist:
            messages.warning(request, "COUPON CODE DOES NOT EXIST")
            return redirect('cart:carts')
        
        if coupon.valid_to < timezone.now().date():
            messages.warning(request, "COUPON CODE IS NOT VALID")
            return redirect('cart:carts')

        if UserCoupon.objects.filter(user=user, coupon_applied=coupon).exists():
            messages.warning(request, "YOU HAVE ALREADY USED THIS COUPON")
            return redirect('cart:carts')

        cart, _ = Cart.objects.get_or_create(user=user)  
        if cart.get_total() < coupon.min_amount:
            messages.warning(request, "MINIMUM CART AMOUNT NOT MET")
            return redirect('cart:carts')
  
        applicable_type = coupon.applicable_type
        if applicable_type == 'Caterogy All':
            # Apply coupon to all categories
            cart.coupon_applied = coupon
            cart.save()
            UserCoupon.objects.create(user=user, coupon_applied=coupon)
            messages.success(request, "COUPON APPLIED SUCCESSFULLY")
            return redirect('cart:carts')
        elif applicable_type == 'Category':
            category = coupon.category
            if CartItem.objects.filter(cart=cart, product__category=category).exists():
                    cart.coupon_applied = coupon
                    cart.save()
                    UserCoupon.objects.create(user=user, coupon_applied=coupon)
                    messages.success(request, "COUPON APPLIED SUCCESSFULLY")
                    return redirect('cart:carts')
            else:
                    messages.warning(request, "COUPON IS NOT APPLICABLE TO SELECTED CATEGORY")
                    return redirect('cart:carts')
        else:
            messages.warning(request, "INVALID APPLICABLE TYPE")
            return redirect('cart:carts')
    return redirect('cart:carts')