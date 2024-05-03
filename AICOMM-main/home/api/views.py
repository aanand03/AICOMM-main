from django.http import JsonResponse
from home.models import Review
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ReviewSerializer

@api_view(['GET'])
def getRoutes(request):
    routes=['GET api/','GET api/reviews']
    return Response(routes)

@api_view(['GET'])
def getReviews(request):
    revs= Review.objects.all()
    serializer= ReviewSerializer(revs,many=True)
    return Response(serializer.data)