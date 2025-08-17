from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ..models import Movie, Review
from ..serializers import ReviewSerializer, ReviewCreateUpdateSerializer
from ..permissions import IsReviewOwner

class ReviewListCreateView(generics.ListCreateAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(
            movie_id=self.kwargs['movie_id']
        ).select_related('user')

    def get_serializer_class(self):
        return ReviewCreateUpdateSerializer if self.request.method == 'POST' else ReviewSerializer

    def perform_create(self, serializer):
        movie = get_object_or_404(Movie, pk=self.kwargs['movie_id'])
        serializer.context['movie'] = movie
        serializer.save()  # el serializer usa request.user

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Review.objects.all().select_related('user')
    serializer_class = ReviewCreateUpdateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsReviewOwner]
