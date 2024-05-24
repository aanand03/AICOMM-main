from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader
from django.shortcuts import HttpResponse
from datetime import datetime
from home.models import Customer
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import requests

from .models import Product, PurchaseHistory ,Review, Cart
from math import ceil
from .customforms import CreateUserForm
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    products = Product.objects.all()
    allProds = []
    catprods = Product.objects.values('p_category')
    cats = set(item['p_category'] for item in catprods)

    for cat in cats:
        prod = Product.objects.filter(p_category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    if request.user.is_authenticated:
        purchase_history_items = PurchaseHistory.objects.filter(user=request.user)
        purchased_product_ids = list(purchase_history_items.values_list('product__id', flat=True))
        top_category_product = purchase_history_items.values('product__sub_category__category') \
                                                      .annotate(total=Count('product__sub_category__category')) \
                                                      .order_by('-total') \
                                                      .first()

        top_category = Product.objects.filter(sub_category__category=top_category_product['product__sub_category__category']) \
                                      .order_by('-id') \
                                      .first() if top_category_product else None

                # Get the top two subcategories
        top_two_subcategories = purchase_history_items.values('product__sub_category') \
                                                    .annotate(total=Count('product__sub_category')) \
                                                    .order_by('-total')[:2]

        # Extract the top subcategory
        top_subcategory_product = top_two_subcategories[0] if len(top_two_subcategories) > 0 else None

        top_subcategory = Product.objects.filter(sub_category=top_subcategory_product['product__sub_category']) \
                                        .order_by('-id') \
                                        .first() if top_subcategory_product else None

        # Extract the second top subcategory
        second_top_subcategory_product = top_two_subcategories[1] if len(top_two_subcategories) > 1 else None

        second_top_subcategory = Product.objects.filter(sub_category=second_top_subcategory_product['product__sub_category']) \
                                                .order_by('-id') \
                                                .first() if second_top_subcategory_product else None

                # Get the top two colors
        top_two_colors = purchase_history_items.values('product__p_color') \
                                            .annotate(total=Count('product__p_color')) \
                                            .order_by('-total')[:2]

        # Extract the top color
        top_color_product = top_two_colors[0] if len(top_two_colors) > 0 else None

        top_color = Product.objects.filter(p_color=top_color_product['product__p_color']) \
                                .order_by('-id') \
                                .first() if top_color_product else None

        # Extract the second top color
        second_top_color_product = top_two_colors[1] if len(top_two_colors) > 1 else None

        second_top_color = Product.objects.filter(p_color=second_top_color_product['product__p_color']) \
                                        .order_by('-id') \
                                        .first() if second_top_color_product else None

        api_urls = [
            'http://localhost:8000/api/reviews'
        ]

        data_list = []
        for api_url in api_urls:
            response = requests.get(api_url)
            if response.status_code == 200:
                data_list.append(response.json())
            else:
                return render(request, '404.html')

        context = {
            'allProds': allProds,
            'purchase_history_items': purchase_history_items,
            'data_list': data_list,
            'top_category': top_category,
            'top_subcategory': top_subcategory,
            'second_top_subcategory' :second_top_subcategory,
            'top_color': top_color,
            'second_top_color': second_top_color,
            'purchased_product_ids': purchased_product_ids,
        }
    else:
        context = {
            'allProds': allProds
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

# importing the signals  app's __init__.py file
default_app_config = 'your_app_name.apps.YourAppConfig'

def default(request):
    #for profile summary section of profile modal dashboard
    purchase_history_items = PurchaseHistory.objects.filter(user=request.user)
    purchased_product_ids = list(purchase_history_items.values_list('product__id', flat=True))
    top_category_product = purchase_history_items.values('product__sub_category__category') \
                                      .annotate(total=Count('product__sub_category__category')) \
                                      .order_by('-total') \
                                      .first()

    if top_category_product:
        top_category = Product.objects.filter(sub_category__category=top_category_product['product__sub_category__category']) \
                                      .order_by('-id') \
                                      .first()
    else:
        top_category = None
    # Get the top bought subcategory
    top_subcategory_product = purchase_history_items.values('product__sub_category') \
                                         .annotate(total=Count('product__sub_category')) \
                                         .order_by('-total') \
                                         .first()

    if top_subcategory_product:
        top_subcategory = Product.objects.filter(sub_category=top_subcategory_product['product__sub_category']) \
                                         .order_by('-id') \
                                         .first()
    else:
        top_subcategory = None
    # Get the top bought color
    top_color_product = purchase_history_items.values('product__p_color') \
                                   .annotate(total=Count('product__p_color')) \
                                   .order_by('-total') \
                                   .first()
    

    if top_color_product:
        top_color = Product.objects.filter(p_color=top_color_product['product__p_color']) \
                                   .order_by('-id') \
                                   .first()
    else:
        top_color = None
    #print(top_category)
   # print("-------------TOP CATEGORY-------------------------")

    #for recommendations section of profile modal dashboard
    api_urls = [
        'http://localhost:8000/api/reviews'
    ]
    
    # List to store response data
    data_list = []
    
    # Fetch data from each API URL
    for api_url in api_urls:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            data_list.append(data)
        else:
            # Handle the error case
            return render(request, '404.html')

    context = {
        'purchase_history_items' : purchase_history_items,
        'data_list': data_list,
        'top_category': top_category,
        'top_subcategory': top_subcategory,
        'top_color': top_color,
        'purchased_product_ids':purchased_product_ids,
    }
    return render(request,"base.html",context)
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
    total = productv.p_price
    ship = 100
    disc = (10/100) * total
    net= total+ship-disc
    #print(productv)
    return render(request, "checkout.html", {'product': productv,'total' : total, 'ship':ship, 'disc':disc,'net':net})

def search(request):
    query = request.GET.get('query')
    if query:
        results = Product.objects.filter(p_name=query)  
    else:
        results = None
    return render(request, 'search.html', {'results': results, 'query': query})

def prodView(request,myid):
    productv=Product.objects.filter(id=myid).first()
    print(productv)
    api_url = 'http://localhost:8000/api/allreviews'
    #api_url = 'https://api.json-generator.com/templates/Q-OWre5hxfoj/data?access_token=ly4gkvvbm8d762l5yhskuwgvdusprxhird8gtjrt'
    response = requests.get(api_url)
    reviews = Review.objects.all().first()
    #print(reviews)
    if response.status_code == 200:
        data = response.json()
        # Process the fetched data as needed
        
    else:
        # Handle the error case
        return render(request, '404.html')
    return render(request, "prodView.html", {'product': productv,'data': data, 'reviews':reviews})

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

def base_test(request):
    return render(request,'base_test.html')

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
                    product=item.product,
                    item_name=item.product.p_name,
                    #item_clothing_id=item.product.clothing_id,
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
           # item_clothing_id=product.clothing_id
            item_cat = product.p_category
            item_price = product.p_price
            item_img = product.p_img
            PurchaseHistory.objects.create(
                user=request.user,
                product=product,
                item_name=item_name,
               # item_clothing_id=item_clothing_id,
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
    #print(rev)
    return render(request, "review.html", {'reviews': reviews})

def mycart(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_items_length = len(cart_items)
    total = sum(item.product.p_price for item in cart_items)
    context = {'cart_items': cart_items,'cart_items_length': cart_items_length}
    return render(request, 'cart.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    messages.success(request, f"{product} has been added to cart!")
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('shop')

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('mycart')

def cart_checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.p_price for item in cart_items)
    ship = 100
    disc = (10/100) * total
    net= total+ship-disc
    context = {'cart_items': cart_items,'total' : total, 'ship':ship, 'disc':disc,'net':net}
    return render(request, 'cart_checkout.html', context)

# API import view
import requests

def api_data_view(request):
    # Importing recommendations for API data
    api_urls = [
        'http://localhost:8000/api/reviews'
        #Dresses
        #'https://api.json-generator.com/templates/G3WUYi8tt5K2/data?access_token=16khqsc164f0dv8c0cesfnsw0f5jrvf22gnjfxun',
        #Jeans
        #'https://api.json-generator.com/templates/-2fOeLk9az48/data?access_token=16khqsc164f0dv8c0cesfnsw0f5jrvf22gnjfxun',
        #Sweaters
       # 'https://api.json-generator.com/templates/pbLRf6skR5ex/data?access_token=16khqsc164f0dv8c0cesfnsw0f5jrvf22gnjfxun',
        #Jackets
        #'https://api.json-generator.com/templates/2pvGLo3pRbDS/data?access_token=16khqsc164f0dv8c0cesfnsw0f5jrvf22gnjfxun',
        #Gauge
        #'https://api.json-generator.com/templates/0CFsNdYQSed_/data?access_token=16khqsc164f0dv8c0cesfnsw0f5jrvf22gnjfxun',
        #Pants
        #'https://api.json-generator.com/templates/J3wtxU1TL0Y_/data?access_token=16khqsc164f0dv8c0cesfnsw0f5jrvf22gnjfxun',
        #Skirts
        #'https://api.json-generator.com/templates/U6Frbs2OoIeH/data?access_token=16khqsc164f0dv8c0cesfnsw0f5jrvf22gnjfxun',
        # Add more API URLs as needed
    ]
    
    # List to store response data
    data_list = []
    
    # Fetch data from each API URL
    for api_url in api_urls:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            data_list.append(data)
        else:
            # Handle the error case
            return render(request, '404.html')

    #added code
    reviews = PurchaseHistory.objects.filter(user=request.user)
    #print(reviews)

    # Process the fetched data as needed
    return render(request, 'recommendations.html', {'data_list': data_list, 'reviews': reviews})

    #recommendations_template = loader.get_template('recommendations.html')
    #recommendations_html = recommendations_template.render({'data_list': data_list, 'reviews': reviews}, request)

    # Render the base_test.html template
    #base_template = loader.get_template('base.html')
    #base_html = base_template.render({'data_list': data_list, 'reviews': reviews, 'recommendations_html': recommendations_html}, request)

    # Create an HttpResponse object with the rendered HTML
    #response = HttpResponse(base_html)

    #return response

    # If no data is fetched or an error occurs, return an empty HttpResponse
    #return HttpResponse()
    
def api_review(request):
    api_url = 'http://localhost:8000/api/allreviews'
    #api_url = 'https://api.json-generator.com/templates/Q-OWre5hxfoj/data?access_token=ly4gkvvbm8d762l5yhskuwgvdusprxhird8gtjrt'
    response = requests.get(api_url)
    reviews = Review.objects.all()
    #print(reviews)
    if response.status_code == 200:
        data = response.json()
        # Process the fetched data as needed
        return render(request, 'api_review.html', {'data': data,'reviews':reviews})
    else:
        # Handle the error case
        return render(request, '404.html')