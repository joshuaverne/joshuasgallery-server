from django.db import models
from django.contrib.auth.models import User


class Exhibition(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class GalleryPiece(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    pub_date = models.DateTimeField('date published to gallery')
    galleries = models.ManyToManyField(Exhibition)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

