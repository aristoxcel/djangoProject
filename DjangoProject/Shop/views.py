from django.shortcuts import render, redirect
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views import View
from django.views.generic.base import TemplateView
from . models import *
from . forms import *
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.
class home(View):
   def get(self, request):
      totalitem = 0
      gentspants= Product.objects.filter(category= 'GP')
      borkha= Product.objects.filter(category= 'BK')
      saree= Product.objects.filter(category= 'S')
      babyfashions= Product.objects.filter(category= 'BF')
      lehenga= Product.objects.filter(category= 'L')
      if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user = request.user))
      return render(request, 'Shop/home.html',{'gentspants':gentspants, 'borkha':borkha, 'saree': saree, 'babyfashions':babyfashions,'lehenga':lehenga, 'totalitem':totalitem})


def search(request):
   if request.method == 'GET':
      src = request.GET.get('src')
      if src:
         product = Product.objects.filter(Q(title__icontains=src)|Q(brand__icontains=src)|Q(category__icontains=src))
         return render(request,'Shop/search.html', {'product':product} )
      else:
         product = Product.objects.all()
         return render(request,'Shop/search.html', {'product':product})

# def home(request):
#      return render(request, 'Shop/home.html')

# def product_detail(request):
#  return render(request, 'Shop/productdetail.html')

class ProductDetailView(View):
  def get(self,request, pk):
    product = Product.objects.get(pk=pk)
    item_already_in_cart = False
    if request.user.is_authenticated:
       item_already_in_cart = Cart.objects.filter(Q(product = product.id) & Q(user = request.user)).exists()
    product.brand = product.brand.replace('_',' ')
    return render(request, 'Shop/productdetail.html', {'product':product, 'item_already_in_cart': item_already_in_cart})

# to add product into cart
@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('showcart')
 
# to show cart from navber or after add to cart
@login_required
def show_cart(request):
   if request.user.is_authenticated:
      user = request.user
      cart = Cart.objects.filter(user=user)
      totalitem =0
      totalitem = len(cart)
      amount = 0.0
      shipping_charge =100
      total_amount = 0.0
      cart_product = [p for p in Cart.objects.all() if p.user == user]
      if cart_product:
         for p in cart_product:
            product_bill = (p.quantity * p.product.discounted_price)
            amount += product_bill
            totalamount =amount + shipping_charge
         return render(request, 'Shop/addtocart.html',{'carts':cart, 'amount':amount, 'totalamount':totalamount, 'totalitem':totalitem})
      else:
         return render(request, 'Shop/emptycart.html')
      

# Plus Cart
def plus_cart(request):
   if request.method == 'GET':
      prod_id = request.GET['prod_id']
      c= Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
      c.quantity += 1
      c.save()
      amount = 0.0
      shipping_charge =100
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      for p in cart_product:
         product_bill = (p.quantity * p.product.discounted_price)
         amount += product_bill
         totalamount =amount + shipping_charge
      
      data = {
         'quantity':c.quantity,
         'amount':amount,
         'totalamount':totalamount
      }
      return JsonResponse(data)
   

def minuscart(request):
   if request.method == 'GET':
      prod_id = request.GET['prod_id']
      c= Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
      c.quantity -= 1
      c.save()
      amount = 0.0
      shipping_charge =100
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      for p in cart_product:
         product_bill = (p.quantity * p.product.discounted_price)
         amount += product_bill
         totalamount =amount + shipping_charge
      
      data = {
         'quantity':c.quantity,
         'amount':amount,
         'totalamount':totalamount
      }
      return JsonResponse(data)


# Remove item from Cart
def remove_cart(request):
   if request.method == 'GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.delete()
      amount = 0.0
      shipping_charge = 100
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      for p in cart_product:
         product_bill = (p.quantity * p.product.discounted_price)
         amount += product_bill
         totalamount = amount + shipping_charge
      
      data = {
         'amount':amount ,
         'totalamount':totalamount
      }
      return JsonResponse(data)



def buy_now(request):
 return render(request, 'Shop/buynow.html')

# def profile(request):
#  return render(request, 'Shop/profile.html')
@method_decorator(login_required, name='dispatch')
class CustomerProfileView(View):
   def get(self, request):
      form = CustomerProfileForm()
      return render(request, 'Shop/profile.html',{'form':form, 'active':'btn-primary'})
   
   def post (self, request):
      form = CustomerProfileForm(request.POST)
      if form.is_valid():
         usr = request.user
         name = form.cleaned_data['name']
         division = form.cleaned_data['division']
         district = form.cleaned_data['district']
         thana = form.cleaned_data['thana']
         villorroad = form.cleaned_data['villorroad']
         zipcode = form.cleaned_data['zipcode']
         reg= Customer(user= usr, name=name, division=division, district=district, thana=thana, villorroad=villorroad, zipcode=zipcode)
         reg.save()
         messages.success(request, 'Congratulation ! Successfully Your Profile Updated.')
      return render(request, 'Shop/profile.html',{'form':form, 'active':'btn-primary'})

@login_required
def address(request):
 add = Customer.objects.filter(user =request.user)
 return render(request, 'Shop/address.html',{'add':add, 'active':'btn-primary'})





def lehenga(request, data=None):
   if data == None:
      lehengas = Product.objects.filter(category ='L')
   elif data == 'Lubnan' or data =='rayans':
      lehengas =Product.objects.filter(category ='L').filter(brand=data)
   elif data == 'below':
      lehengas =Product.objects.filter(category ='L').filter(discounted_price__lt= 20000)
   elif data == 'above':
      lehengas =Product.objects.filter(category ='L').filter(discounted_price__gt= 20000)
   return render(request, 'Shop/lehenga.html', {'lehengas':lehengas})


def saree(request, data=None):
   if data == None:
      sari = Product.objects.filter(category ='S')
   elif data == 'Meesho' or data =='Suvash':
      sari =Product.objects.filter(category ='S').filter(brand=data)
   elif data == 'below':
      sari =Product.objects.filter(category ='S').filter(discounted_price__lte= 1500)
   elif data == 'above':
      sari =Product.objects.filter(category ='S').filter(discounted_price__gt= 1500)
   return render(request, 'Shop/saree.html', {'sari':sari})

def borkha(request, data=None):
   if data == None:
      borka = Product.objects.filter(category ='BK')
   elif data == 'Sagorika' or data =='Noborupa_Fashion_House':
      borka =Product.objects.filter(category ='BK').filter(brand=data)
   elif data == 'below':
      borka =Product.objects.filter(category ='BK').filter(discounted_price__lt= 2000)
   elif data == 'above':
      borka =Product.objects.filter(category ='BK').filter(discounted_price__gt= 2000)
   return render(request, 'Shop/borkha.html', {'borka':borka})


def baby_fashion(request, data=None):
   if data == None:
      baby = Product.objects.filter(category ='BF')
   elif data == 'Alam_Garments':
      baby =Product.objects.filter(category ='BF').filter(brand=data)
   elif data == 'Baby-Boy' or data =='Baby-Girl':
      baby =Product.objects.filter(category ='BF').filter(title=data)
   elif data == 'below':
      baby =Product.objects.filter(category ='BF').filter(discounted_price__lt= 700)
   elif data == 'above':
      baby =Product.objects.filter(category ='BF').filter(discounted_price__gt= 700)
   return render(request, 'Shop/baby.html', {'baby':baby})


def pants(request, data=None):
   if data == None:
      pant = Product.objects.filter(category ='GP')
   elif data == 'Rakib_Fashion' or data =='Sunmon':
      pant =Product.objects.filter(category ='GP').filter(brand=data)
   elif data == 'below':
      pant =Product.objects.filter(category ='GP').filter(discounted_price__lte= 1500)
   elif data == 'above':
      pant =Product.objects.filter(category ='GP').filter(discounted_price__gt= 1500)
   return render(request, 'Shop/pants.html', {'pant':pant})
  


# login page// instead of def function here used class based function loginView
# def loginpage(request):
#      if request.method == 'POST':
#         login_form = AuthenticationForm(request=request, data= request.POST)
#         if login_form.is_valid():
#             username = login_form.cleaned_data['username']
#             password = login_form.cleaned_data['password']
#             user = authenticate(username= username, password=password)
#             if user is not None:
#                 login(request,user)
#                 return redirect(home)
#      else:
#         login_form = AuthenticationForm()
#      return render(request, 'Shop/login.html', {'lg':login_form})


# def customerregistration(request):
#      if request.method == 'POST':
#         regfrom = UserCreationForm(request.POST)
#         if regfrom.is_valid():
#           regfrom.save()
#           return redirect('successful')
#      else:
#         regfrom = UserCreationForm()
#      return render(request, 'Shop/customerregistration.html', {'form':regfrom})

# // Registration Form //
class customerregistration(View):
  def get (self, request):
    regfrom = Registration_form()
    return render(request, 'Shop/customerregistration.html', {'form':regfrom})
  
  def post(self, request):
    regfrom = Registration_form(request.POST)
    if regfrom.is_valid():
      messages.success(request, 'Congratulation ! Registration Successfully done')
      regfrom.save()
    return render(request, 'Shop/customerregistration.html', {'form':regfrom})


#Successful msg after registration
class successful(TemplateView):
  template_name = 'Shop/success.html'

#// Check out // Place order
@login_required
def checkout(request):
 user = request.user
 address = Customer.objects.filter(user = user)
 cart_items = Cart.objects.filter(user = user)
 amount = 0.0
 shipping_charge =100
 total_amount = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user == user]
 if cart_product:
   for p in cart_product:
      product_bill = (p.quantity * p.product.discounted_price)
      amount += product_bill
   totalamount =amount + shipping_charge
 return render(request, 'Shop/checkout.html', {'address':address, 'cart_items':cart_items, 'totalamount':totalamount})



def paymentdone(request):
   user = request.user
   cust_id = request.GET.get('custid')
   customer = Customer.objects.get(id=cust_id)
   cart = Cart.objects.filter(user=user)
   for c in cart:
      OrderPlaced(user=user, customer=customer, product= c.product, quantity= c.quantity).save()
      c.delete()
   return redirect('orders')

@login_required
def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'Shop/orders.html', {'order_placed':op})

#user logout function // instead of def function here used class based function logoutView
# def userlogout(request):
#     logout(request)
#     return redirect('home')