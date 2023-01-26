from django.db import models


class Exhibition(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class GalleryPiece(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published to gallery')
    galleries = models.ManyToManyField(Exhibition)

    def __str__(self):
        return self.title

