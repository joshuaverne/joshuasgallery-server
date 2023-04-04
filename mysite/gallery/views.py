import http

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage

from .models import GalleryPiece, Exhibition
from .forms import NewGalleryPieceForm

PIECE_IMG_DIR = "piece-images/"
ALLOWED_IMG_EXTENSIONS = ["jpg", "jpeg", "png"]
MAX_IMG_SIZE_BYTES = 10000000

def index(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED)

    pieces_list = GalleryPiece.objects.filter(user=request.user)
    output = ', '.join(p.title for p in pieces_list)
    return render(request=request,
                  template_name="mysite/my_gallery_dashboard.html",
                  context={'form': NewGalleryPieceForm(), 'pieces': output})


def exhibition_detail(request, exhibition_id):
    return HttpResponse("You're looking at exhibition %s." % exhibition_id)


def piece_detail(request, piece_id):
    return HttpResponse("You're looking at piece %s." % piece_id)


def get_new_gallery_piece(request):
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to do that.")

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

            # redirect to a new URL:
            return HttpResponseRedirect("/gallery")

    # if a GET (or any other method) we'll redirect to the gallery page
    else:
        return HttpResponseRedirect("/gallery")

def validate_new_gallery_piece_form(form_data, file_data):
    if len(form_data) != 2 or len(file_data) != 1:
        raise ValidationError("Incorrect number of fields in form data")

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
