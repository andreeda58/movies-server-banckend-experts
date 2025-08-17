from rest_framework import serializers
from .models import Movie, Review

# --- Reviews ---
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'user', 'rating', 'comment', 'created_at')


class ReviewCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('rating', 'comment')

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError('Rating must be 1–5')
        return value

    def create(self, validated_data):
        # Un review por (user, movie)
        user = self.context['request'].user
        movie = self.context['movie']
        review, _ = Review.objects.update_or_create(
            user=user, movie=movie, defaults=validated_data
        )
        return review


# --- Movies ---
class MovieSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)
    poster = serializers.ImageField(required=False, allow_null=True)
    owner = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'description', 'poster', 'director', 'main_actors',
            'release_year', 'average_rating', 'reviews_count', 'owner',
            'created_at', 'updated_at'
        )

    def to_representation(self, instance):

        data = super().to_representation(instance)
        poster_url = data.get('poster')
        request = self.context.get('request')
        if poster_url and request and not poster_url.startswith('http'):
            data['poster'] = request.build_absolute_uri(poster_url)
        return data
