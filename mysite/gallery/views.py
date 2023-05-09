import http, logging

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseBadRequest
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib import messages

from .models import GalleryPiece, Exhibition

PIECE_IMG_DIR = "piece-images/"
ALLOWED_IMG_EXTENSIONS = ["jpg", "jpeg", "png"]
PIECE_TITLE_LEN_MAX = 500
PIECE_DESC_LEN_MAX = 1000
EXHIB_TITLE_LEN_MAX = 200
EXHIB_DESC_LEN_MAX = 1000
MAX_IMG_SIZE_BYTES = 10000000

logger = logging.getLogger(__name__)


def index(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED)

    pieces_list = GalleryPiece.objects.filter(user=request.user)
    exhibs_list = Exhibition.objects.filter(user=request.user)
    return render(request=request,
                  template_name="mysite/my_gallery_dashboard.html",
                  context={'pieces': pieces_list, 'exhibs': exhibs_list})


def pieces_list_view(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED)

    pieces_list = GalleryPiece.objects.filter(user=request.user)

    return render(request=request,
                  template_name="mysite/gallery_pieces_list.html",
                  context={'pieces': pieces_list})


def piece_detail(request, piece_id):
    if not request.user.is_authenticated:
        return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED)

    piece = GalleryPiece.objects.get(id=piece_id)

    return render(request=request,
                  template_name="mysite/gallery_piece_detail.html",
                  context={'piece': piece})


def exhibitions_list_view(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED)

    exhibs_list = Exhibition.objects.filter(user=request.user)

    return render(request=request,
                  template_name="mysite/gallery_exhibitions_list.html",
                  context={'exhibs': exhibs_list})


def exhibition_detail(request, exhibition_id):
    return HttpResponse("You're looking at exhibition %s." % exhibition_id)


def get_new_gallery_piece(request):
    if not request.user.is_authenticated:
        return HttpResponseNotAllowed("You must be logged in to do that.")

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        r_post = request.POST
        r_files = request.FILES

        # check whether it's valid:
        try:
            validate_new_gallery_piece_form(dict(list(r_post.items())[1:]), r_files)
        except ValidationError:
            return HttpResponseBadRequest("Form data invalid")
        else:
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

            messages.success(request, "Piece created successfully.")

            return HttpResponseRedirect("/gallery")

    # if a GET (or any other method) we'll redirect to the gallery page
    else:
        return HttpResponseRedirect("/gallery")


def new_gallery_piece(request):
    if not request.user.is_authenticated:
        return HttpResponseNotAllowed("You must be logged in to do that.")

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        r_post = request.POST
        r_files = request.FILES

        # check whether it's valid:
        try:
            validate_new_gallery_piece_form(dict(list(r_post.items())[1:]), r_files)
        except ValidationError:
            return HttpResponseBadRequest("Form data invalid")
        else:
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

            messages.success(request, "Piece created successfully.")

            return HttpResponseRedirect("/gallery/pieces")

    # if a GET (or any other method) we'll redirect to the gallery page
    else:
        return render(request=request,
                      template_name="mysite/gallery_piece_new.html")


def edit_gallery_piece(request, piece_id):
    if not request.user.is_authenticated:
        return HttpResponseNotAllowed("You must be logged in to do that.")

    piece = GalleryPiece.objects.get(id=piece_id)

    if not piece.user == request.user:
        return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED)

    actual_title = piece.title
    title = piece.title
    desc = piece.description
    img = piece.image
    piece_id = piece.id

    title_error = ""
    desc_error = ""
    img_error = ""

    if request.method == 'POST':
        if 'pieceTitle' not in request.POST or 'pieceDescription' not in request.POST:
            return HttpResponseBadRequest("Required fields not in post data")

        title = request.POST['pieceTitle']
        desc = request.POST['pieceDescription']

        title_c = False
        desc_c = False
        img_c = False

        if title != piece.title:
            title_c = True
        if desc != piece.description:
            desc_c = True
        if 'pieceImage' in request.FILES:
            img_c = True
            img = request.FILES['pieceImage']

        if not (title_c or desc_c or img_c):
            messages.error(request, "No changes were made.")
            return HttpResponseRedirect("/gallery/pieces/" + str(piece_id) + "/edit")

        save = True

        if title_c:
            try:
                validate_gallery_piece_title(title)
            except ValidationError as e:
                title_error = e.message
                save = False
        if desc_c:
            try:
                validate_gallery_piece_description(desc)
            except ValidationError as e:
                desc_error = e.message
                save = False
        if img_c:
            try:
                validate_gallery_piece_image(img)
            except ValidationError as e:
                img_error = e.message
                save = False

        if save:
            piece.title = title
            piece.description = desc
            piece.image = img
            piece.save()
            messages.success(request, "Changes successfully applied")

            actual_title = title
            return render(request=request,
                          template_name="mysite/gallery_piece_detail_edit.html",
                          context={'actual_title': actual_title,
                                   'piece_title': title,
                                   'piece_desc': desc,
                                   'piece_img': img,
                                   'title_error': title_error,
                                   'desc_error': desc_error,
                                   'img_error': img_error})

        else:
            messages.error(request, "Invalid Piece info. Please correct the errors below.")

    return render(request=request,
                  template_name="mysite/gallery_piece_detail_edit.html",
                  context={'actual_title': actual_title,
                           'piece_title': title,
                           'piece_desc': desc,
                           'piece_img': img,
                           'piece_id': piece_id,
                           'title_error': title_error,
                           'desc_error': desc_error,
                           'img_error': img_error})


def delete_gallery_piece(request, piece_id):
    if not request.user.is_authenticated:
        return HttpResponseNotAllowed("You must be logged in to do that.")

    piece = GalleryPiece.objects.get(id=piece_id)

    if not piece.user == request.user:
        return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED)

    piece.delete()

    messages.success(request, "Piece deleted successfully.")

    return HttpResponseRedirect("/gallery/pieces")


def validate_gallery_piece_title(t):
    if len(t) > PIECE_TITLE_LEN_MAX:
        raise ValidationError("Title is too long (Max 200 characters)")

    if len(t) < 1:
        raise ValidationError("Title cannot be blank")


def validate_gallery_piece_description(d):
    if len(d) > PIECE_DESC_LEN_MAX:
        raise ValidationError("Description is too long (Max 1000 characters)")


def validate_gallery_piece_image(img):
    img_ext = img.name.split(".")[-1]
    if img_ext not in ALLOWED_IMG_EXTENSIONS:
        raise ValidationError("Invalid file format")

    if img.size > MAX_IMG_SIZE_BYTES:
        raise ValidationError("File too large")


def validate_new_gallery_piece_form(form_data, file_data):
    if len(file_data) != 1:
        raise ValidationError("Incorrect number of fields in FILES data: " + str(len(file_data)) + " (expected 1)")

    if len(form_data) != 2:
        raise ValidationError("Incorrect number of fields in POST data: " + str(len(form_data)) + " (expected 2)")

    title = form_data['pieceTitle']
    desc = form_data['pieceDescription']
    img = file_data['pieceImage']

    if len(title) > PIECE_TITLE_LEN_MAX:
        raise ValidationError("Title too long")

    if len(desc) > PIECE_DESC_LEN_MAX:
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
    if len(form_data) != 2:
        raise ValidationError("Incorrect number of fields in FORM data: " + str(len(form_data)) + " (expected 2)")

    title = form_data['exhibitionTitle']
    desc = form_data['exhibitionDescription']

    if len(title) > EXHIB_TITLE_LEN_MAX:
        raise ValidationError("Exhibition title too long")

    if len(desc) > EXHIB_DESC_LEN_MAX:
        raise ValidationError("Exhibition description too long")
