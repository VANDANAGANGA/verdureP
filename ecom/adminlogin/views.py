from datetime import date, timedelta, timezone
import json
from django.shortcuts import get_object_or_404, render,redirect
from user.models import CustomUser,Product,ProductSize,Category,CustomUserManager,ProfilePhoto
from checkout.models  import Order,OrderItems
from cart.models import Coupon,UserCoupon
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.db.models import Sum
from django.template.loader import render_to_string
from io import BytesIO
from django.http import HttpResponse
from xhtml2pdf import pisa



# Create your views here.
def home(request):
    today = date.today()
    total_payment_amount = Order.objects.filter(order_date__date__lte=today).aggregate(total=Sum('payment_amount'))
    orders = Order.objects.filter(order_date__date__lte=today)
    total_amount = total_payment_amount['total'] if total_payment_amount['total'] else 0
    category_totals = OrderItems.objects.values('product__category__category_name').annotate(total_amount=Sum('amount'))
    category=Category.objects.all()
    cod_payment_amount = Order.objects.filter(order_date__date__lte=today, payment_method='COD').aggregate(total=Sum('payment_amount'))
    cod_total_amount = cod_payment_amount['total'] if cod_payment_amount['total'] else 0

# Calculate total payment amount for PayPal orders
    paypal_payment_amount = Order.objects.filter(order_date__date__lte=today, payment_method='PayPal').aggregate(total=Sum('payment_amount'))
    paypal_total_amount = paypal_payment_amount['total'] if paypal_payment_amount['total'] else 0

    context= {
        'total_payment_amount': total_amount,
        'orders': orders,
        'category':category,
        'category_totals': category_totals,
        'cod_total_amount': cod_total_amount,
        'paypal_total_amount': paypal_total_amount,
    }
    return  render(request,'admin/dashboard.html',context)


def adminsignin(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials or access denied.')
            return redirect('adminsignin')
    
    return render(request, 'admin/adminlogin.html')

def adminsignout(request):
    logout(request)
    return redirect('adminsignin')

def userdisplay(request):
    stu=CustomUser.objects.all()
    return render(request,'admin/userdisplay.html',{'stus':stu})

def search_user(request):
    if request.method=='POST':
        query=request.POST['query']
        user=CustomUser.objects.filter(Q(first_name__icontains=query)|Q(email__icontains=query)|Q(mobile__contains=query))
        return render(request,'admin/search_user.html',{'user':user})
    
def user_block(request,id):
    if request.method == 'POST':
         user = CustomUser.objects.get(pk=id)
         user.is_active =False
         user.save()
    return redirect('userdisplay')

def user_unblock(request,id):
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=id)
        user.is_active=True
        user.save()
    return redirect('userdisplay')

def categorylist(request):
    stu=Category.objects.all()
    return render(request,'admin/categorylist.html',{'stu':stu})

def delete_category(request,id):
    if request.method=='POST':
        pi=Category.objects.get(pk=id)
        pi.delete()
        return redirect('categorylist')

def search_category(request):
    if request.method=='POST':
        query=request.POST['query']
        category=Category.objects.filter(Q(category_name__icontains=query)|Q(id__contains=query))
        return render(request,'admin/searchcategory.html',{'category':category})


def add_category(request):
    if request.method == 'POST':
        category_name = request.POST['categoryname']
        if Category.objects.filter(category_name=category_name).exists():
            error_message = 'Category name already exists.'
            return render(request, 'admin/categorylist.html', {'error_message': error_message})
        else:
            category = Category.objects.create(category_name=category_name)
            stu=Category.objects.all()
            return render(request,'admin\categorylist.html',{'stu':stu})  # Redirect to category list page

    return render(request, 'admin/categorylist.html')


def addproduct(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        # Retrieve data from the form

        product_name = request.POST.get('productName')
        category_name=request.POST.get('category')
        print(category_name)
        category = Category.objects.get(category_name=category_name)
        category_id = category.pk
        # category = request.POST.get('category')
        description = request.POST.get('description')
        image = request.FILES.get('productphoto')
        sizes = ['small', 'medium', 'large']
        if Product.objects.filter(product_name=product_name):
            return render(request,'admin\product_add.html')
        else:
        # Create the product object
             if image:
                product = Product(product_name=product_name,category=category, description=description,image=image)
                product.save()
                product_id = Product.id
             else: 
                  product = Product(product_name=product_name,category=category, description=description)
                  product.save()  
        # Create the product sizes and associate them with the product
        for size in sizes:
            checkbox = request.POST.get(f'checkbox-{size}')
            if checkbox:
                price = request.POST.get(f'price-{size}')
                offer_price = request.POST.get(f'offer-price-{size}')
                count = request.POST.get(f'productCount-{size}')
                image = request.FILES.get(f'image-{size}')
                product_size = ProductSize(product_id=product, size=size, price=price, offer_price=offer_price,quantity=count,product_photo=image)
                product_size.save()

        # Redirect to a success page or perform any additional actions

    return render(request, 'admin\product_add.html',{'categories':categories})
        # Redirect to a success page or perform any additional actions
def product_display(request):
    stu=Category.objects.all()
    products=Product.objects.all()
    product_sizes = ProductSize.objects.all()
    return render(request,'admin\productlist.html',{'products':products})

def search_product(request):
    if request.method=='POST':
        query=request.POST['query']
        product=Product.objects.filter(Q(product_name__icontains=query))
        print(request,product)
        return render(request,'admin/product_search.html',{'product':product})

def delete_product(request,id):
     if request.method == 'POST':
        product = get_object_or_404(Product, pk=id)
        product.soft_delete()
        return redirect('product_display')
     
def undo_product(request,id):
     if request.method == 'POST':
        product = get_object_or_404(Product, pk=id)
        product.undo()
        return redirect('product_display')     

def edit_product(request, id):
    try:
        product = Product.objects.get(pk=id)
        size=product.productsize_set.all()
        category=Category.objects.all()
        print(request,size)
        context={
            'product':product,
            'sizes':size,
            'categories':category
        }
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product not found")

    if request.method == 'POST':
        product_name = request.POST.get('productName')
        category_id = request.POST.get('categoryId')
        category = get_object_or_404(Category, pk=category_id)        
        description = request.POST.get('description')
        photo= request.FILES.get('productphoto')
        sizes = ['small', 'medium', 'large']
        # Update the product details
        product.product_name = product_name
        product.category = category
        product.description = description
        if photo:
           product.image=photo
        product.save()
        
        for size in sizes:
            checkbox = request.POST.get(f'checkbox-{size}')
            if checkbox:
                price = request.POST.get(f'price-{size}')
                offer_price = request.POST.get(f'offer-price-{size}')
                count = request.POST.get(f'productCount-{size}')
                image = request.FILES.get(f'image-{size}')

                # Update or create the product size
                product_size, _ = ProductSize.objects.get_or_create(product_id=product, size=size)
                product_size.price = price
                product_size.offer_price = offer_price
                product_size.quantity = count
                if image:
                    product_size.product_photo = image
                product_size.save()

        return redirect('product_display')  # Redirect to a success page or product list view

    # If the request method is not POST, render the edit product form with the current product details
    return render(request, 'admin/edit_product.html', context)

def order_display(request):
    stu=CustomUser.objects.all()
    order=Order.objects.all()
    order_items = OrderItems.objects.all()
    context={
         'order':order,
         'order_items':order_items
    }
    return render(request,'admin\order.html',context) 



def coupon(request):
    coupons=Coupon.objects.all()
    category=Category.objects.all()
    context={
        'coupons':coupons,
        'category':category,
    }
    return render(request,'admin\coupon.html',context) 

def add_coupon(request):
    if request.method=='POST':
        coupon_code=request.POST.get('code')
        coupon_description = request.POST.get('description')
        discount_type = request.POST.get('coupon_status')
        discount = request.POST.get('discount')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        category = request.POST.get('category')
        min_amount=request.POST.get('min_amount')
        active = bool(request.POST.get('active'))
        category_selection = request.POST.get('categorySelection')
        
        coupon = Coupon(
                coupon_code=coupon_code,
                description=coupon_description,
                discount_type=discount_type,
                discount=discount,
                valid_from=start_date,
                valid_to=end_date,
                applicable_type=category,
                category=category_selection,
                active=active,
                min_amount=min_amount
            )
        coupon.save()
        return redirect('coupon')
    

def change_orderitem_status(request):
    if request.method == 'POST':
        order_item_id = request.POST.get('order_item_id')
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('order_status')

        try:
            order_item = OrderItems.objects.get(id=order_item_id)
            order_item.order_status = new_status
            order_item.save()
            if new_status=='Cancelled':
                 product_size = order_item.product_size
                 product_size.quantity += order_item.quantity
                 product_size.save()
            order = Order.objects.get(order_id=order_id)
            has_active_items = OrderItems.objects.filter(order_no__order_id=order_id).exclude(order_status=new_status).exists()
            if not has_active_items:
                print(7676767676767676767676)
                order.order_status=new_status
            order.save()
        except OrderItems.DoesNotExist:
            pass
        return redirect('order_display') 
    return render(request, 'admin/order.html')


def change_order_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('order_status')
        print(new_status,5555555555555555555)
        try:
            order = Order.objects.get(order_id=order_id)
            order_items = OrderItems.objects.filter(order_no=order)
            order.order_status = new_status
            order.save()
            for order_item in order_items:
                # if order_item.order_status != 'Cancelled':
                    order_item.order_status = new_status
                    order_item.save()

        except OrderItems.DoesNotExist:
            pass
        return redirect('order_display') 
    return render(request, 'admin/order.html')








    
def totalsales(request):
    today = date.today()
    total_payment_amount = Order.objects.filter(order_date__date__lte=today).aggregate(total=Sum('payment_amount'))
    orders = Order.objects.filter(order_date__date__lte=today)
    total_amount = total_payment_amount['total'] if total_payment_amount['total'] else 0
    context= {
        'total_payment_amount': total_amount,
        'orders': orders,
        'duration':"TOTAL",
    }
    return render(request,'admin/salesreport.html',context)

def todaysales(request):
    today = date.today()
    total_payment_amount = Order.objects.filter(order_date__date=today).aggregate(total=Sum('payment_amount'))
    orders = Order.objects.filter(order_date__date=today)
    total_amount = total_payment_amount['total'] if total_payment_amount['total'] else 0
    context= {
        'total_payment_amount': total_amount,
        'orders': orders,
        'duration':"TODAY"
    }
    return render(request,'admin/salesreport.html',context)
from datetime import datetime, date, time

def weeksales(request):
    today = date.today()
    
    start_date = today - timedelta(days=7)
    print(start_date)  # Get the start date (today - 6 days)
    end_date = datetime.combine(today, time.max)

    print(end_date,999999999999999999999999999999999)
    orders = Order.objects.filter(order_date__range=[start_date,end_date])
    total_amount = sum(order.payment_amount for order in orders)
    context= {
        'total_payment_amount': total_amount,
        'orders': orders,
        'duration': "WEEK"
    }
    return render(request,'admin/salesreport.html',context)
    
def monthlysales(request):
    today = date.today()
    start_date = today.replace(day=1)  # Get the first day of the current month
    end_date = datetime.combine(today, time.max)
    start_date -= timedelta(days=1)
    orders = Order.objects.filter(order_date__range=[start_date,end_date])
    total_amount = sum(order.payment_amount for order in orders)
    context= {
        'total_payment_amount': total_amount,
        'orders': orders,
        'duration':"MONTH"
    }
    return render(request,'admin/salesreport.html',context)

def yearlysales(request):
    today = date.today()
    start_date = today.replace(month=1, day=1)  
    end_date = today.replace(month=12, day=31)
    orders = Order.objects.filter(order_date__range=[start_date, end_date])
    total_amount = sum(order.payment_amount for order in orders)
    context= {
        'total_payment_amount': total_amount,
        'orders': orders,
        'duration':"YEAR"
    }
    return render(request,'admin/salesreport.html',context)



def fromtosales(request):
    if request.method == 'POST':
        from_date_str = request.POST.get('fromDate')
        to_date_str = request.POST.get('toDate')
        print(from_date_str)
        print(to_date_str)
    
    from_date = date.fromisoformat(from_date_str)
    to_date = datetime.combine(date.fromisoformat(to_date_str), time.max)
    print(from_date,888888888888888)
    print(to_date,88888888888888888)
    orders = Order.objects.filter(order_date__range=[from_date, to_date])
    total_amount = sum(order.payment_amount for order in orders)
    todate=to_date.date()
    context= {
        'total_payment_amount': total_amount,
        'orders': orders,
        'duration': "FROM: " + str(from_date) + " TO: " + str(todate)

    }
    return render(request,'admin/salesreport.html',context)
    












def pdf_generator(request):
    if request.method == 'POST':
        # Retrieve the data from the request body
        body = json.loads(request.body)
        orders = body.get('orders', [])
        total_payment_amount = body.get('total_payment_amount', 0)
        
        # Generate the PDF using the data
       
        context = {
            'orders': orders,
            'total_payment_amount': total_payment_amount,
        }
        # Render the template
        rendered_report = render_to_string('admin/sales_report.html', context)

        # Create PDF using xhtml2pdf
        pdf_file = BytesIO()
        pisa.CreatePDF(rendered_report, dest=pdf_file)

        # Set the appropriate response headers
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

        # Get the PDF content from the BytesIO buffer and write it to the response
        pdf_file.seek(0)
        response.write(pdf_file.getvalue())

        return response


