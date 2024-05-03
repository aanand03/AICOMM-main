from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import HttpResponse
from datetime import datetime
from home.models import Customer
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
import requests

from .models import Product, PurchaseHistory ,Review, Cart
from math import ceil
from .customforms import CreateUserForm
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    products=Product.objects.all()
    #print(products)
    #n=len(products)
    #nSlides=(n//3)+ceil((n/3)-(n//3))
    #params={'no_of_slides':nSlides, 'range':range(1,nSlides), 'products': products}
    #allProds=[[products,range(1,nSlides),nSlides],[products,range(1,nSlides),nSlides]]
    allProds = []
    catprods = Product.objects.values('p_category')
    # print(catprods) -> all the categories for each object
    # print(type(catprods)) -> quesryset
    cats = set()
    # cats should be a set coz a set doesn't allow duplicate values in it
    for item in catprods:
        # print(item) -> {'category' -> 'category value'}
        # print(type(item)) -> dictionary
        cats.add(item['p_category'])
    # print(cats) -> set with unique categories
    # print(type(cats)) -> set

    for cat in cats:
        prod = Product.objects.filter(p_category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n//4))
        allProds.append([
            prod, range(1, nSlides), nSlides
        ])

    context = {
        'allProds' : allProds
    }
    return render(request, 'index.html', context)
    
    #return HttpResponse("Welcome to home page")
from django.shortcuts import get_object_or_404

def category(request,cate):
    products = Product.objects.filter(p_category=cate)
    allProds = []
   # catprods = Product.objects.values('p')
    
  #  cats = set()
    
  #  for item in catprods:
       
  #      cats.add(item['p_category'])
   
   # for cat in cats:
     #   prod = Product.objects.filter(p_category=cat)
    n = len(products)
    nSlides = n//4 + ceil((n/4) - (n//4))
    allProds.append([
            products, range(1, nSlides), nSlides
        ])
    return render(request, 'category.html', {'products': products, 'category': cate,'allProds': allProds})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .customforms import UserProfileForm
from .models import UserProfile

@login_required
def update_profile(request):
    profile = UserProfile.objects.get_or_create_profile(request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile has been updated')
            # Add a success message or redirect as needed
            return redirect('shop')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'update_profile.html', {'form': form})
         

# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Make sure to import the signals in your app's __init__.py file
default_app_config = 'your_app_name.apps.YourAppConfig'


def bottom(request):
    return render(request,"bottom.html")

def tops(request):
    return render(request,"tops.html")

def trending(request):
    return render(request,"trending.html")

def cart(request):
    return render(request,"cart.html")

def checkout(request,myid):
    productv=Product.objects.filter(id=myid).first()
    print(productv)
    return render(request, "checkout.html", {'product': productv})

def search(request):
    query = request.GET.get('query')
    if query:
        results = Product.objects.filter(p_name=query)  # Adjust based on your model fields
    else:
        results = None
    return render(request, 'search.html', {'results': results, 'query': query})

def prodView(request,myid):
    productv=Product.objects.filter(id=myid).first()
    print(productv)
    return render(request, "prodView.html", {'product': productv})

def customer(request):
    if request.method=="POST":
        email=request.POST.get('email')
        name=request.POST.get("name")
        query=request.POST.get("query")
        Customer_ins = Customer(email=email,name=name,query=query,date=datetime.today())
        Customer_ins.save()
        messages.success(request, "Your feedback has been sent!")
    return render(request,"customer.html")

def loginPage(request):
    if request.method =="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user=authenticate(request, username=username, password=password)
        if(user is not None):
            auth_login(request,user)
            return redirect('shop')
        else:
            messages.info(request,'username or password is not correct')

    return render(request,"login.html")

def logoutPage(request):
    logout(request)
    return redirect('login')

def signin(request):
    forms=CreateUserForm()
    context ={'forms':forms}
    if request.method=="POST":
        forms=CreateUserForm(request.POST)
        if(forms.is_valid()):
            forms.save()
            user=forms.cleaned_data.get('username')
            messages.success(request, "Account created successfully for user " + user )
            return redirect('login')
        else:
           # print(forms.errors)
            messages.success(request, "Error!")
    return render(request,"signindex.html",context)



#def buy_now(request):
  #  if request.method == 'POST':
        # Assuming you're passing item details in the request
   #     item_name = request.POST.get('item_name')
        # Capture other item details as needed

        # Save purchase details to the database
    #    PurchaseHistory.objects.create(item_name=item_name, user=request.user)
        
        # You can also do any additional processing or redirection here
        # For example, redirect to the purchase history page
  #      return render(request, 'purchase_history.html')
    
  

def buy_now(request):
    if request.method == 'POST':
        if 'from_cart' in request.POST:
           
        # Handle the request from the checkout
            cart_items = Cart.objects.filter(user=request.user)
            for item in cart_items:
                PurchaseHistory.objects.create(
                    user=request.user,
                    item_name=item.product.p_name,
                    item_cat=item.product.p_category,
                    item_price=item.product.p_price,
                    item_img=item.product.p_img
                )
            cart_items.delete()
            return redirect('history')
        else:
             # Handle the request from the cart
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)
            item_name = product.p_name
            item_cat = product.p_category
            item_price = product.p_price
            item_img = product.p_img
            PurchaseHistory.objects.create(
                user=request.user,
                item_name=item_name,
                item_price=item_price,
                item_cat=item_cat,
                item_img=item_img
            )
            return redirect('history')
    return render(request, 'purchase_history.html')

def history(request):
    purchase_history_items = PurchaseHistory.objects.filter(user=request.user)
    #print("Number of Purchase History Items:", purchase_history_items.count())
    return render(request, 'history.html', {'purchase_history_items': purchase_history_items})

def review(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        review_text = request.POST.get('review')
        rating = request.POST.get('rating')
        item = PurchaseHistory.objects.get(id=item_id)
        Review.objects.create(item=item, user=request.user, review_text=review_text, rating=rating)
    return redirect('history')

def rev(request):
    reviews = Review.objects.filter(user=request.user)
    print(rev)
    return render(request, "review.html", {'reviews': reviews})

def mycart(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_items_length = len(cart_items)
    context = {'cart_items': cart_items,'cart_items_length': cart_items_length}
    return render(request, 'cart.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('shop')

def cart_checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    context = {'cart_items': cart_items}
    return render(request, 'cart_checkout.html', context)

# API import view
def api_data_view(request):
    #api_url = 'http://localhost:8000/api/reviews'
    api_url = 'https://api.json-generator.com/templates/Q-OWre5hxfoj/data?access_token=ly4gkvvbm8d762l5yhskuwgvdusprxhird8gtjrt'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        # Process the fetched data as needed
        return render(request, 'recommendations.html', {'data': data})
    else:
        # Handle the error case
        return render(request, 'error.html')
    
def api_review(request):
    api_url = 'http://localhost:8000/api/reviews'
    #api_url = 'https://api.json-generator.com/templates/Q-OWre5hxfoj/data?access_token=ly4gkvvbm8d762l5yhskuwgvdusprxhird8gtjrt'
    response = requests.get(api_url)
    reviews = Review.objects.filter(user=request.user)
    print(reviews)
    if response.status_code == 200:
        data = response.json()
        # Process the fetched data as needed
        return render(request, 'api_review.html', {'data': data,'reviews':reviews})
    else:
        # Handle the error case
        return render(request, 'error.html')