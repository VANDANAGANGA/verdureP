from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from cart.models import Cart,CartItem,Wallet
from user.models import CustomUser,Product,ProductSize,ProfileAddress,ProfilePhoto
from .models import Order,OrderItems
import razorpay
from ecom.settings import RAZOR_KEY_ID, RAZOR_KEY_SECRET 
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='signin')
def checkout(request):
    user = request.user
    if user is None:
        return render(request,'user/signup.html')
    
    cart=Cart.objects.get(user=user)if user else None
    cart_items =CartItem.objects.filter(cart__user=user)
    address=ProfileAddress.objects.filter(user=user)
    balance=Wallet.objects.get(user=user)
    context ={
         'cart_items':cart_items,
         'cart':cart,
         'address':address,
         'balance':balance,
    }
    return render(request,'user/checkout.html',context)


def order(request):
    user=request.user
    if user is None:
         return render(request,'user/signup.html')
    payment_method = request.POST.get('payment_modal2')
    if not payment_method:
            messages.error(request, 'Please select a payment method.')
            return redirect('checkout:checkout')
    name = request.POST.get('modalname')
    house_name = request.POST.get('modalhouse_name')
    city = request.POST.get('modalcity')
    street = request.POST.get('modalstreet')
    postal_code = request.POST.get('modalzip')
    state = request.POST.get('modalstate')
    country = request.POST.get('modalcountry')
    phone_number = request.POST.get('modalnumber')
    wallet=request.POST.get('wallet_modal')
    print(wallet,9999999999999999999999999)
    cart_items =CartItem.objects.filter(cart__user=user)
    cart = Cart.objects.get(user=user)
    total_mrp = cart.get_total_price()  
    offer_price = cart.get_price_difference()
    coupon_discount = cart.coupon_discount()
    delivery_charge = cart.get_shipping_charge() 
    payment_amount = cart.get_total()
    balance=Wallet.objects.get(user=user)
    print(balance,555555555555)
    payment_status='Pending'
    if payment_method == 'Paypal':
        payment_status = 'Completed'
    if wallet=='true':
        if balance.balance > cart.get_total():
            payment_amount=0
            balance.balance=balance.balance-cart.get_total()
            balance.save()
        else:
            payment_amount=cart.get_total()-balance.balance
            balance.balance=0
            balance.save()    
    profile_address = ProfileAddress.objects.filter(user=user, name=name, house_name=house_name, city=city, street=street, postal_code=postal_code, state=state, country=country, phone_number=phone_number).first()
    if not profile_address:
        profile_address = ProfileAddress(
            user=user,
            name=name,
            phone_number=phone_number,
            house_name=house_name,
            street=street,
            city=city,
            state=state,
            country=country,
            postal_code=postal_code
        )
        profile_address.save()

        # Create a new order instance
    order = Order(
            user=request.user,
            order_status='Confirmed',
            payment_status=payment_status,
            payment_method=payment_method,
            name=name,
            house_name=house_name,
            city=city,
            street=street,
            postal_code=postal_code,
            state=state,
            country=country,
            phone_number=phone_number,
            total_mrp=total_mrp,
            offer_price=offer_price,
            coupon_discount=coupon_discount,
            delivery_charge=delivery_charge,
            payment_amount=payment_amount
            
        )
    order.save()
    print(order.payment_amount,7777777777777777777777777777)
    for cart_item in cart_items:
            order_item = OrderItems(
                order_no=order,
                product=cart_item.product,
                product_size=cart_item.product_size,
                product_name=cart_item.product.product_name,
                order_status='Confirmed',
                size=cart_item.product_size.size,
                product_price=cart_item.product_size.price,
                product_offer_price=cart_item.product_size.offer_price,
                product_photo=cart_item.product_size.product_photo,
                quantity=cart_item.quantity,
                amount=cart_item.get_subtotal(),
            )
            order_item.save()
    product = cart_item.product
    product_size = ProductSize.objects.get(product_id=product, size=cart_item.product_size.size)
    product_size.quantity -= cart_item.quantity
    product_size.save()
    cart.delete()
    return render(request,'user/codsuccess.html') 
         
def razorpay_payment(request,id):
    user=request.user
    if user is None:
         return render(request,'user/signup.html')
    cart = Cart.objects.get(user=user)
    payment_amount = cart.get_total()*100
    wallet=Wallet.objects.get(user=user)
    if id==1:
        if wallet.balance>payment_amount:
            payment_amount=0
            wallet.balance=wallet.balance-(payment_amount/100)
            wallet.save()
        else:    
            payment_amount=payment_amount-wallet.balance*100
            wallet.balance=0
            wallet.save()
    
    client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))
    DATA = {
    "amount": float(payment_amount),
    "currency": "INR",
    "receipt": "receipt#1",
    "notes": {
        "key1": "value3",
        "key2": "value2"
    }
    }
    order = client.order.create(data=DATA)
    res = {
        'success': True,
        'key_id': RAZOR_KEY_ID,
        'amount': float(payment_amount),
        'order_id': order['id'],
        'name': cart.user.name,
        'email': cart.user.email,
        'mobile': cart.user.mobile,
    }
    return JsonResponse(res)
    
def userorder(request):
      user=request.user
      order=Order.objects.filter(user=user)
      order_items=OrderItems.objects.filter(order_no__in=order)
      try:
        profile_pic = ProfilePhoto.objects.get(user=user)
      except ProfilePhoto.DoesNotExist:
        profile_pic = None
      contex={
      'user':user,     
      'order':order,
      'order_items':order_items,
      'profile_pic':profile_pic,
      }
      return render(request,'user/profileorder.html',contex)

def order_details(request,order_id):
     order = get_object_or_404(Order, order_id=order_id)
     order_items = OrderItems.objects.filter(order_no=order)
    
     address_data = {
        'name': order.name,
        'phone_number': str(order.phone_number),
        'house_name': order.house_name,
        'street': order.street,
        'city': order.city,
        'state': order.state,
        'country': order.country,
        'postal_code': order.postal_code
     }
     order_item_details = []
     for order_item in order_items:
        item_detail = {
            'id': order_item.id,
            'product_name': order_item.product_name,
            'product_image': order_item.product_photo.url,
            'product_quantity' :order_item.quantity,
            'product_price':order_item.amount,
            'order_status':order_item.order_status,
            # Add other details of the order item as needed
        }
        order_item_details.append(item_detail)
        print(order_item_details,55555555555555555555555555555555555)
     response_data = {
        'order_id': order.order_id,
        'order_date': order.order_date,
        'payment_amount': order.payment_amount,
        'payment_method': order.payment_method,
        'order_status':order.order_status,
        'order_items':order_item_details,
        'address': address_data,
        # Add other order details as needed
        }
     return JsonResponse(response_data)


def cancelorderitem(request):
    if request.method =='POST':
        id=request.POST.get('itemid') 
        order_id=request.POST['order_id']   
    order_item = OrderItems.objects.get(id=id)
    try:
        wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(user=request.user)

    if order_item is not None:
        order_item.order_status = 'Cancelled'
        order_item.save()
        product_size = order_item.product_size
        product_size.quantity += order_item.quantity
        if product_size.offer_price:
            wallet.balance=(product_size.offer_price*85)/100
        else:
            wallet.balance=(product_size.price*85)/100   
        product_size.save()
        wallet.save()
        order = Order.objects.get(order_id=order_id)
        has_active_items = OrderItems.objects.filter(order_no__order_id=order_id).exclude(order_status='Cancelled').exists()
        if not has_active_items:
             order.order_status='Cancelled'
             order.save()
        return redirect('checkout:userorder')
    else:
        return HttpResponse("Item not found.")
    
def cancelorder(request):
      if request.method == 'POST':
        id = request.POST.get('order_id')
        order = Order.objects.get(order_id=id)
        order.order_status = 'Cancelled'
        order.save()
        order_items = OrderItems.objects.filter(order_no=order)
        try:
            wallet = Wallet.objects.get(user=request.user)
        except Wallet.DoesNotExist:
            wallet = Wallet.objects.create(user=request.user)

        amount=0
        for item in order_items:
            product = item.product_size
            product.quantity += item.quantity
            if product.offer_price:
                amount+=product.offer_price
            else:    
                amount+=product.offer_price
            product.save()
            amount=(amount*85)/100
            wallet.balance=amount
            wallet.save()
            item.order_status = 'Cancelled'
            item.save()
      return redirect('checkout:userorder')

def returnproduct(request):
    if request.method == 'POST':
        item_id=request.POST.get('itemid') 
        id = request.POST.get('order_id')
        order = Order.objects.get(order_id=id)
        return render(request,'user/reason.html',{'order_id': id, 'item_id': item_id})
     

def returnorderitem(request):
    if request.method =='POST':
        id=request.POST.get('itemid') 
        order_id=request.POST['order_id']
        return_reasons = {
            'defective': 'Defective or damaged product',
            'poor_quality': 'Poor quality or not as described',
            'wrong_item': 'Item is not what I ordered',
            'dislike': 'Don\'t like the product',
            }      
        return_reason = request.POST.get('return_reason')
        other_reason = return_reasons.get(return_reason, '')
        if return_reason == 'other':
            other_reason = request.POST.get('other_reason', '')    
    order_item = OrderItems.objects.get(id=id)
    if order_item is not None:
        order_item.order_status = 'Returned'
        order_item.return_problem = other_reason
        order_item.save()
        order = Order.objects.get(order_id=order_id)
        has_active_items = OrderItems.objects.filter(order_no__order_id=order_id).exclude(order_status__in=['Returned', 'Cancelled']).exists()
        if not has_active_items:
             order.order_status= 'Returned'
             order.save()
        return redirect('checkout:userorder')
    else:
        return HttpResponse("Item not found.")
    