from django.db import models


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    genres = models.JSONField(default=list)
    year = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title