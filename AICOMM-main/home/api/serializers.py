from rest_framework.serializers import ModelSerializer
from home.models import Review

class ReviewSerializer(ModelSerializer):
    class Meta:
        model=Review
        fields="__all__"