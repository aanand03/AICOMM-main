"""
URL configuration for hello project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views

from django.conf import settings
from django.conf.urls.static import static 

admin.site.site_header="WELCOME TO AICOMM"
admin.site.site_title="AICOMM ADMIN PORTAL"
admin.site.index_title="AICOMM"



urlpatterns = [
    path("",views.default,name=""),
    path("shop",views.index,name="shop"),
    path("base_test",views.base_test,name="base_test"),
    path("update_profile",views.update_profile,name="update_profile"),
    path("product<int:myid>", views.prodView, name="prodView"),
    path("bottom",views.bottom,name="bottom"),
    path("tops",views.tops,name="tops"),
    path("trending",views.trending,name="trending"),
    path("customer",views.customer,name="customer"),
    path("mycart",views.mycart,name="mycart"),
    path("buy_now",views.buy_now,name="buy_now"),
    path("checkout<int:myid>",views.checkout,name="checkout"),
    path('cart_checkout', views.cart_checkout, name='cart_checkout'),
    path('search', views.search, name='search'),
    path("login",views.loginPage,name="login"),
    path("logout",views.logoutPage,name="logout"),
    path("signin",views.signin,name="signin"),
    path("history",views.history,name="history"),
    path("review",views.review,name="review"),
    path("recommendations",views.api_data_view,name="recommendations"),
    path("api_review",views.api_review,name="api_review"),
    path("rev",views.rev,name="rev"),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path("category<str:cate>",views.category,name="category")
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
