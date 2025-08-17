from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..models import Movie, Review
from ..serializers import ReviewSerializer, ReviewCreateUpdateSerializer
from ..permissions import IsReviewOwner, IsOwnerOrReadOnly
from django.db.models import Avg, Count
from ..serializers import MovieSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(movie_id=self.kwargs['movie_id']).select_related('user')

    def get_serializer_class(self):
        return ReviewCreateUpdateSerializer if self.request.method == 'POST' else ReviewSerializer

    def perform_create(self, serializer):
        movie = get_object_or_404(Movie, pk=self.kwargs['movie_id'])
        serializer.context['movie'] = movie
        serializer.save()

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all().select_related('user')
    serializer_class = ReviewCreateUpdateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsReviewOwner]


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().annotate(
        average_rating=Avg('reviews__rating'),
        reviews_count=Count('reviews')
    )
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)