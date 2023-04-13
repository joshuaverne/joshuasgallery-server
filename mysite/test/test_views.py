from django.test import RequestFactory, TestCase, Client
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AnonymousUser, User

from gallery.views import get_new_gallery_piece


class GalleryPieceFormViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="jacob", email="jacob@…", password="top_secret"
        )

    def test_get_view_redirect(self):
        request = self.factory.get("/gallery/get_new_gallery_piece")

        request.user = self.user

        response = get_new_gallery_piece(request)

        self.assertEqual(302, response.status_code)

    def test_create_piece(self):
        title = "x" * 500
        desc = "x" * 1000

        with open("test/images/woody.jpg", "rb") as fp:
            test_post_data = {'placeholder': "PLACEHOLDER",
                              'pieceTitle': title,
                              'pieceDescription': title,
                              'pieceImage': fp}
            request = self.factory.post("/gallery/add_gallery_piece", test_post_data)

            request.user = self.user

            response = get_new_gallery_piece(request)

        self.assertEqual(302, response.status_code)

    def create_piece_title_too_long(self):
        title = "x" * 501

        with open("test/images/woody.jpg", "rb") as fp:
            test_post_data = {'placeholder': "PLACEHOLDER",
                              'pieceTitle': title,
                              'pieceDescription': "woody from toy story",
                              'pieceImage': fp}
            request = self.factory.post("/gallery/add_gallery_piece", test_post_data)

            request.user = self.user

            get_new_gallery_piece(request)

    def test_create_piece_title_too_long(self):
        self.assertRaises(ValidationError, self.create_piece_title_too_long)

    def create_piece_description_too_long(self):
        desc = "x" * 1001

        with open("test/images/woody.jpg", "rb") as fp:
            test_post_data = {'placeholder': "PLACEHOLDER",
                              'pieceTitle': "title",
                              'pieceDescription': desc,
                              'pieceImage': fp}
            request = self.factory.post("/gallery/add_gallery_piece", test_post_data)

            request.user = self.user

            get_new_gallery_piece(request)

    def test_create_piece_description_too_long(self):
        self.assertRaises(ValidationError, self.create_piece_description_too_long)

