from django.db import models
from django.contrib.auth.models import User


class Exhibition(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class GalleryPiece(models.Model):
    title = models.CharField(max_length=500, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    pub_date = models.DateTimeField('date published to gallery')
    galleries = models.ManyToManyField(Exhibition, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='piece-images', null=True)

    def clean(self):
        if self.title == "":
            self.title = "Untitled " + self.pub_date.__str__().split(" ")[0]

    def __str__(self):
        return self.title
