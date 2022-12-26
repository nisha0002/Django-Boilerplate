from ast import Return
from itertools import product
from unicodedata import category
from django.http import JsonResponse
from django.shortcuts import redirect, render  #get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
#from django.contrib.auth.decorators import login_required
from django.views import View

from app.models import Customer, Product, Cart, OrderPlaced , Product# Variation, CartItem
from .forms import CustomerRegistrationForm , AuthenticationForm , CustmerProfileForm
from django.contrib import messages
from django.db.models import Q


#def home(request):
 #return render(request, 'app/home.html')

class ProductView(View):
    def get(self,requset):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        laptop = Product.objects.filter(category='L')
        mobile = Product.objects.filter(category='M')
        return render(requset,'app/home.html',{"topwears":topwears,"bottomwears":bottomwears,"laptop":laptop,"mobile":mobile})

#def product_detail(request):
class ProductDetailView(View):
    def get(self, request,pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html',{'product':product})








def add_to_cart(request):

    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save() 
    return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart =  Cart.objects.filter(user=user)
        print(cart)
        amount = 0.0
        shipping_amount = 70.0
        total_price = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        #print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.selling_price)
                amount += tempamount 
                totalamount = amount +  shipping_amount
            return render(request,'app/addtocart.html',{'carts':cart,'totalamount':totalamount, 'amount':amount})
        else:
            return render(request, 'app/emptycart.html')    

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount 
        

        data = {
                'quantity':c.quantity,
                'amount': amount,
                'totalamount': amount +  shipping_amount,

            }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount 
            

        data = {
                'quantity':c.quantity,
                'amount': amount,
                'totalamount': amount +  shipping_amount,

            }
        return JsonResponse(data)        

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount 
            

        data = {
                
                'amount': amount,
                'totalamount': amount +  shipping_amount,

            }
        return JsonResponse(data)







def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add, 'active':'btn-primary'})

def orders(request):
 return render(request, 'app/orders.html')



def mobile(request, data=None):
    if data == None:
        mobile = Product.objects.filter(category='M')
    elif data == 'samsung' or data == 'redmi':
        mobile = Product.objects.filter(category='M').filter(brand=data)
    elif data  == 'below':
        mobile = Product.objects.filter(category='M').filter(selling_price__lt=100000)
    elif data == 'above':
        mobile = Product.objects.filter(category='M').filter(selling_price__gt=100000)
    return render(request, 'app/mobile.html',{'mobile':mobile})

def laptop(request, data=None):
    if data == None:
        laptop = Product.objects.filter(category='L')
    elif data == 'lenovo' or data == 'apple' or data == 'dell':
       laptop = Product.objects.filter(category='L').filter(brand=data)
    elif data  == 'below':
        laptop = Product.objects.filter(category='L').filter(selling_price__lt=100000)
    elif data == 'above':
        laptop = Product.objects.filter(category='L').filter(selling_price__gt=100000)
    return render(request, 'app/laptop.html',{'laptop': laptop}) 

def topwears(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'nykee' or data == 'zudio' or data == 'ajio':
       topwears = Product.objects.filter(category='TW').filter(brand=data)
    elif data  == 'below':
        topwears= Product.objects.filter(category='TW').filter(selling_price__lt=300)
    elif data == 'above':
        topwears = Product.objects.filter(category='TW').filter(selling_price__gt=300)
    return render(request, 'app/topwears.html',{'topwears': topwears}) 

def bottomwears(request, data=None):
    if data == None:
        bottomwears = Product.objects.filter(category='BW')
    elif data == 'ajio' or data == 'zara' or data == 'puma':
       bottomwears = Product.objects.filter(category='BW').filter(brand=data)
    elif data  == 'below':
        bottomwears= Product.objects.filter(category='BW').filter(selling_price__lt=300)
    elif data  == 'above':
        bottomwears= Product.objects.filter(category='BW').filter(selling_price__gt=300)

    return render(request, 'app/bottomwears.html',{'bottomwears': bottomwears}) 



def login(request):
 return render(request, 'app/login.html')


class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self,request):

        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'registered successfully.')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})
            


def checkout(request):
    user = request.user
    add  = Customer.objects.filter(user=user)
    cart_item = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount 
            totalamount = amount + shipping_amount
        
    
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_item':cart_item})

def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")        
        


    

class ProfileView(View):
    def get(self,request):
        form = CustmerProfileForm()
        return render(request,'app/profile.html',{'form': form, 'active':'btn-primary'})

    def post(self,request):
        form = CustmerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']  
            locality = form.cleaned_data['locality']  
            state = form.cleaned_data['state']  
            city = form.cleaned_data['city']  
            pincode = form.cleaned_data['pincode'] 
            reg = Customer(user=usr, name=name,locality=locality, city=city, state=state, pincode=pincode)
            reg.save()   
            messages.success(request,'profile updated!!')
            return render(request,'app/profile.html',{'form':form, 'active':'btn-primary'})

