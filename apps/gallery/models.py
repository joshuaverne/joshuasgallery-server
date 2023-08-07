from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Exhibition(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class GalleryPiece(models.Model):
    title = models.CharField(max_length=500, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    pub_date = models.DateTimeField('date published to gallery')
    galleries = models.ManyToManyField(Exhibition, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='piece-images', null=True)
    thumbnail = ImageSpecField(source='image',
                               processors=[ResizeToFill(100, 50)],
                               format='JPEG',
                               options={'quality': 60})

    def clean(self):
        if self.title == "":
            self.title = "Untitled " + self.pub_date.__str__().split(" ")[0]

    def __str__(self):
        return self.title
