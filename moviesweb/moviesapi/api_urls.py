# moviesapi/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views.movies import MovieViewSet
from .api_views.reviews import ReviewListCreateView, ReviewDetailView

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')

urlpatterns = [
    path('', include(router.urls)),
    path('movies/<int:movie_id>/reviews/', ReviewListCreateView.as_view(), name='movie-reviews'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]
