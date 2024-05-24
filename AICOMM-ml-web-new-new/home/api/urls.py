from django.urls import path
from . import views



urlpatterns = [
    path('',views.getRoutes),
    path('reviews',views.getReviews),
    path('allreviews',views.getAllReviews)
]
