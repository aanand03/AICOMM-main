from django.contrib import admin
from home.models import Customer, Product, PurchaseHistory, Review ,UserProfile, Cart, Category, Sub_Category
# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(PurchaseHistory)
admin.site.register(Review)
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Sub_Category)