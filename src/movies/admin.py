from django.contrib import admin

from .models import Movie, UserMoviePreferences

admin.site.register(Movie)
admin.site.register(UserMoviePreferences)
# Register your models here.
