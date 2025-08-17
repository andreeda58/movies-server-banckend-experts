from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'release_year')
    search_fields = ('title', 'director', 'actors')
