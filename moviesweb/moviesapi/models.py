from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# moviesapi/models.py
from django.db import models
from django.conf import settings

class Movie(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='movies',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    director = models.CharField(max_length=120, blank=True)
    main_actors = models.TextField(blank=True, help_text='Comma-separated')
    release_year = models.PositiveIntegerField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['-created_at']


class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('movie', 'user')
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.user} → {self.movie} ({self.rating})'
