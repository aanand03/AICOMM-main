from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    email=models.CharField(max_length=122)
    name=models.CharField(max_length=122)
    query=models.TextField()
    date=models.DateField()

    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.name
    
class Sub_Category(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    sname=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.sname+" from "+self.category.name



from django.db import models

class Product(models.Model):
    p_id = models.AutoField
    p_name = models.CharField(max_length=122)
    p_desc = models.CharField(max_length=122)
    p_color = models.CharField(max_length=122)
    p_date = models.DateField()
    p_price = models.FloatField(null=True)
    p_img = models.ImageField(upload_to="static/images", default="")
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE, null=True)
    
    # Add the p_category field
    p_category = models.CharField(max_length=100, null=True, blank=True)  # Adjust max_length as needed
    
    def __str__(self):
        return self.p_name+" - "+self.p_category
    
    class Meta:
        ordering = ['p_category', 'p_name']
    
    def save(self, *args, **kwargs):
        # Set p_category based on sub_category
        if self.sub_category:
            self.p_category = self.sub_category.category.name
        else:
            self.p_category = None
        
        # Call the save method of the superclass
        super().save(*args, **kwargs)


class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    item_name = models.CharField(max_length=100)
   # item_clothing_id = models.IntegerField(null=True)
    item_cat = models.CharField(max_length=100)
    item_price = models.FloatField(max_length=100)
    item_img=models.ImageField(upload_to="static/images",default="")
    
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.item_name}"
    
class Review(models.Model):
    item = models.ForeignKey(PurchaseHistory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.item.item_name}"    
    


from django.contrib.auth.models import User
from django.db import models

class UserProfileManager(models.Manager):
    def get_or_create_profile(self, user):
        try:
            profile = self.get(user=user)
        except self.model.DoesNotExist:
            profile = self.create(user=user)
        return profile

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    objects = UserProfileManager()
    def __str__(self):
        return self.user.username


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.p_name} ({self.quantity})"