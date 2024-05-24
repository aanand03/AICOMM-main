# from rest_framework.serializers import ModelSerializer
# from home.models import Review

# class ReviewSerializer(ModelSerializer):
#     class Meta:
#         model=Review
#         fields="__all__"



from rest_framework import serializers
from home.models import Category, Sub_Category, Product, PurchaseHistory, Review

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""
    class Meta:
        model = Category
        fields = ['name']

class SubCategorySerializer(serializers.ModelSerializer):
    """Serializer for the Sub_Category model."""
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Sub_Category
        fields = ['sname', 'category']

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the Product model."""
    sub_category = SubCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'p_name', 'p_desc', 'p_color', 'p_date', 'p_price', 'p_img', 'sub_category']

class PurchaseHistorySerializer(serializers.ModelSerializer):
    """Serializer for the PurchaseHistory model."""
    product = ProductSerializer(read_only=True)  # Serializing product details using ProductSerializer

    class Meta:
        model = PurchaseHistory
        fields = ['id', 'user', 'product', 'item_name', 'item_cat', 'item_price', 'item_img', 'timestamp']

   # def to_representation(self, instance):
   #     representation = super().to_representation(instance)
   #     item_img = representation.pop('item_img', None)
   #     if item_img:
    #        representation['item_img'] = str(item_img)
    #    return representation
    
class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for the Review model."""
   
    purchase_history_details = PurchaseHistorySerializer(source='item', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'review_text', 'rating', 'created_at', 'purchase_history_details']
