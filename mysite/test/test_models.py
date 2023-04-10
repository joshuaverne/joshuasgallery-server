from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from gallery.models import Exhibition, GalleryPiece


class GalleryPieceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        john = User.objects.create(username="john")
        GalleryPiece.objects.create(title="The Wave", description="A Painting", pub_date=timezone.now(), user=john)

    def test_title_max_length(self):
        piece = GalleryPiece.objects.get(id=1)
        max_length = piece._meta.get_field("title").max_length
        self.assertEqual(max_length, 500)

    def test_description_max_length(self):
        piece = GalleryPiece.objects.get(id=1)
        max_length = piece._meta.get_field("description").max_length
        self.assertEqual(max_length, 1000)
