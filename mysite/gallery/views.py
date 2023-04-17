import http, logging

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseBadRequest
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import GalleryPiece, Exhibition

PIECE_IMG_DIR = "piece-images/"
ALLOWED_IMG_EXTENSIONS = ["jpg", "jpeg", "png"]
MAX_IMG_SIZE_BYTES = 10000000

logger = logging.getLogger(__name__)


def index(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED)

    pieces_list = GalleryPiece.objects.filter(user=request.user)
    return render(request=request,
                  template_name="mysite/my_gallery_dashboard.html",
                  context={'pieces': pieces_list})


def exhibition_detail(request, exhibition_id):
    return HttpResponse("You're looking at exhibition %s." % exhibition_id)


def piece_detail(request, piece_id):
    return HttpResponse("You're looking at piece %s." % piece_id)


def get_new_gallery_piece(request):
    if not request.user.is_authenticated:
        return HttpResponseNotAllowed("You must be logged in to do that.")

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        r_post = request.POST
        r_files = request.FILES

        # check whether it's valid:
        if validate_new_gallery_piece_form(dict(list(r_post.items())[1:]), r_files):
            piece_title = r_post['pieceTitle']
            piece_desc = r_post['pieceDescription']
            piece_image = r_files['pieceImage']

            # construct a new gallery piece with the form data
            new_gallery_piece = GalleryPiece(title=piece_title,
                                             description=piece_desc,
                                             pub_date=timezone.now(),
                                             user=request.user,
                                             image=piece_image)
            new_gallery_piece.clean()

            # save the new gallery piece to the database
            new_gallery_piece.save()

            return render(request=request,
                          template_name="mysite/my_gallery_dashboard.html",
                          context={'pieces': GalleryPiece.objects.filter(user=request.user),
                                   'messages': ["Successfully created new piece: " + piece_title]})

    # if a GET (or any other method) we'll redirect to the gallery page
    else:
        return HttpResponseRedirect("/gallery")


def validate_new_gallery_piece_form(form_data, file_data):
    if len(file_data) != 1:
        raise ValidationError("Incorrect number of fields in FILES data: " + str(len(file_data)) + " (expected 1)")

    if len(form_data) != 2:
        raise ValidationError("Incorrect number of fields in POST data: " + str(len(form_data)) + " (expected 2)")

    title = form_data['pieceTitle']
    desc = form_data['pieceDescription']
    img = file_data['pieceImage']

    if len(title) > 500:
        raise ValidationError("Title too long")

    if len(desc) > 1000:
        raise ValidationError("Description too long")

    img_ext = img.name.split(".")[-1]
    if img_ext not in ALLOWED_IMG_EXTENSIONS:
        raise ValidationError("Invalid file format: " + img_ext)

    if img.size > MAX_IMG_SIZE_BYTES:
        raise ValidationError("File too large")

    return True


def get_new_exhibition(request):
    if not request.user.is_authenticated:
        return HttpResponseNotAllowed("You must be logged in to do that.")

    if request.method == 'POST':
        r_post = request.POST

        # validate
        try:
            validate_new_exhibition_form(dict(list(r_post.items())[1:]))
        except ValidationError:
            return HttpResponseBadRequest("Form data invalid")
        else:
            exhib_title = r_post['exhibitionTitle']
            exhib_desc = r_post['exhibitionDescription']

            # construct a new exhibition with the form data
            new_exhibition = Exhibition(title=exhib_title,
                                        description=exhib_desc,
                                        user=request.user)

            new_exhibition.save()

            # redirect to a new URL:
            return HttpResponseRedirect("/gallery")

    # if a GET (or any other method) we'll redirect to the gallery page
    else:
        return HttpResponseRedirect("/gallery")


def validate_new_exhibition_form(form_data):
    if len(form_data) != 3:
        raise ValidationError("Incorrect number of fields in FORM data: " + str(len(form_data)) + " (expected 3)")

    title = form_data['exhibitionTitle']
    desc = form_data['exhibitionDescription']
    pieces = form_data['exhibitionPieces']

    if len(title) > 200:
        raise ValidationError("Exhibition title too long")

    if len(desc) > 1000:
        raise ValidationError("Exhibition description too long")
