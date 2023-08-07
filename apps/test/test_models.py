from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from gallery.models import Exhibition, GalleryPiece


class GalleryPieceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.john = User.objects.create(username="john")
        cls.piece = GalleryPiece.objects.create(title="The Wave",
                                                description="A Painting",
                                                pub_date=timezone.now(),
                                                user=cls.john)

    def test_title_max_length(self):
        max_length = self.piece._meta.get_field("title").max_length
        self.assertEqual(max_length, 500)

    def test_description_max_length(self):
        max_length = self.piece._meta.get_field("description").max_length
        self.assertEqual(max_length, 1000)
