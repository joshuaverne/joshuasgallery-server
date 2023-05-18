import http

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
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

FORBIDDEN_MSG = "You do not have access to this."


def index(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED)

    pieces_list = GalleryPiece.objects.filter(user=request.user)
    exhibs_list = Exhibition.objects.filter(user=request.user)
    return render(request=request,
                  template_name="mysite/my_gallery_dashboard.html",
                  context={'pieces': pieces_list, 'exhibs': exhibs_list})


# Gallery Piece


def pieces_list_view(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED, reason="You must be logged in to do that.")

    pieces_list = GalleryPiece.objects.filter(user=request.user)

    return render(request=request,
                  template_name="mysite/gallery_pieces_list.html",
                  context={'pieces': pieces_list})


def piece_detail(request, piece_id):
    if not request.user.is_authenticated:
        return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED, reason="You must be logged in to do that.")

    piece = GalleryPiece.objects.get(id=piece_id)

    if not request.user == piece.user:
        return HttpResponseForbidden(reason=FORBIDDEN_MSG)

    return render(request=request,
                  template_name="mysite/gallery_piece_detail.html",
                  context={'piece': piece})


def new_gallery_piece(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED, reason="You must be logged in to do that.")

    created_title = ""
    created_desc = ""
    uploaded_img = None
    title_error = ""
    desc_error = ""
    img_error = ""

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        r_post = request.POST
        r_files = request.FILES

        if "pieceTitle" not in r_post \
                or "pieceDescription" not in r_post:
            return HttpResponseBadRequest("Required fields not in POST data")

        created_title = r_post["pieceTitle"]
        created_desc = r_post["pieceDescription"]

        save = True

        try:
            validate_gallery_piece_title(created_title)
        except ValidationError as e:
            title_error = e.message
            save = False

        try:
            validate_gallery_piece_description(created_desc)
        except ValidationError as e:
            desc_error = e.message
            save = False

        if "pieceImage" not in r_files:
            img_error = "You must upload an image."
            save = False
        else:
            uploaded_img = r_files["pieceImage"]

            try:
                validate_gallery_piece_image(uploaded_img)
            except ValidationError as e:
                img_error = e.message
                save = False

        if save:
            # construct a new gallery piece with the form data
            created_gallery_piece = GalleryPiece(title=created_title,
                                                 description=created_desc,
                                                 pub_date=timezone.now(),
                                                 user=request.user,
                                                 image=uploaded_img)
            created_gallery_piece.clean()

            # save the new gallery piece to the database
            created_gallery_piece.save()

            messages.success(request, "Piece created successfully.")

            return HttpResponseRedirect("/gallery/pieces/")
        else:
            messages.error(request, "Invalid Piece info. Please correct the errors below.")

    # if a GET (or any other method) we'll render the new gallery piece form
    return render(request=request,
                  template_name="mysite/gallery_piece_new.html",
                  context={'created_title': created_title,
                           'created_desc': created_desc,
                           'title_error': title_error,
                           'desc_error': desc_error,
                           'img_error': img_error})


def edit_gallery_piece(request, piece_id):
    if not request.user.is_authenticated:
        return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED, reason="You must be logged in to do that.")

    piece = GalleryPiece.objects.get(id=piece_id)

    if not piece.user == request.user:
        return HttpResponseForbidden(reason=FORBIDDEN_MSG)

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
            return HttpResponseRedirect("/gallery/pieces/" + str(piece_id) + "/edit/")

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
        return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED, reason="You must be logged in to do that.")

    piece = GalleryPiece.objects.get(id=piece_id)

    if not piece.user == request.user:
        return HttpResponseForbidden(reason=FORBIDDEN_MSG)

    piece.delete()

    messages.success(request, "Piece deleted successfully.")

    return HttpResponseRedirect("/gallery/pieces/")


# Exhibition


def exhibitions_list_view(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED, reason="You must be logged in to do that.")

    exhibs_list = Exhibition.objects.filter(user=request.user)

    return render(request=request,
                  template_name="mysite/exhibitions_list.html",
                  context={'exhibs': exhibs_list})


def exhibition_detail(request, exhibition_id):
    if not request.user.is_authenticated:
        return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED, reason="You must be logged in to do that.")

    exhib = Exhibition.objects.get(id=exhibition_id)

    if not exhib.user == request.user:
        return HttpResponseForbidden(reason=FORBIDDEN_MSG)

    return render(request=request,
                  template_name='mysite/exhibition_detail.html',
                  context={'exhib': exhib})


def new_exhibition(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED, reason="You must be logged in to do that.")

    created_title = ""
    created_desc = ""
    title_error = ""
    desc_error = ""

    if request.method == 'POST':
        r_post = request.POST

        if "exhibitionTitle" not in r_post or "exhibitionDescription" not in r_post:
            return HttpResponseBadRequest("Required fields not in POST data")

        created_title = r_post["exhibitionTitle"]
        created_desc = r_post["exhibitionDescription"]

        save = True

        try:
            validate_exhibition_title(created_title)
        except ValidationError as e:
            title_error = e.message
            save = False

        try:
            validate_exhibition_description(created_desc)
        except ValidationError as e:
            desc_error = e.message
            save = False

        if save:
            # construct a new exhibition with the form data
            created_exhibition = Exhibition(title=created_title,
                                            description=created_desc,
                                            user=request.user)

            created_exhibition.save()

            messages.success(request, "Exhibition created successfully.")

            # redirect to a new URL:
            return HttpResponseRedirect("/gallery/exhibitions")
        else:
            messages.error(request, "Invalid Exhibition info. Please correct the errors below.")

    # if a GET or invalid form input, render the new exhibition form
    return render(request=request,
                  template_name="mysite/exhibition_new.html",
                  context={'created_title': created_title,
                           'created_desc': created_desc,
                           'title_error': title_error,
                           'desc_error': desc_error})


def edit_exhibition(request, exhibition_id):
    if not request.user.is_authenticated:
        return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED, reason="You must be logged in to do that.")

    exhib = Exhibition.objects.get(id=exhibition_id)

    if not exhib.user == request.user:
        return HttpResponseForbidden(reason=FORBIDDEN_MSG)

    actual_title = exhib.title
    title = exhib.title
    desc = exhib.description

    title_error = ""
    desc_error = ""

    if request.method == 'POST':
        if 'exhibTitle' not in request.POST or 'exhibDesc' not in request.POST:
            return HttpResponseBadRequest("Required fields not in post data")

        title = request.POST['exhibTitle']
        desc = request.POST['exhibDesc']

        title_c = False
        desc_c = False

        if title != exhib.title:
            title_c = True
        if desc != exhib.description:
            desc_c = True

        if not (title_c or desc_c):
            messages.error(request, "No changes were made.")
            return HttpResponseRedirect("/gallery/exhibitions/" + str(exhibition_id) + "/edit/")

        save = True

        if title_c:
            try:
                validate_exhibition_title(title)
            except ValidationError as e:
                title_error = e.message
                save = False

        if desc_c:
            try:
                validate_exhibition_description(desc)
            except ValidationError as e:
                desc_error = e.message
                save = False

        if save:
            exhib.title = title
            exhib.description = desc
            exhib.save()

            messages.success(request, "Changes successfully applied")

            actual_title = title

        else:
            messages.error(request, "Invalid Exhibition info. Please correct the errors below.")

    return render(request=request,
                  template_name="mysite/exhibition_edit.html",
                  context={'actual_title': actual_title,
                           'exhib_title': title,
                           'exhib_desc': desc,
                           'exhib_id': exhibition_id,
                           'title_error': title_error,
                           'desc_error': desc_error})


def delete_exhibition(request, exhibition_id):
    if not request.user.is_authenticated:
        return HttpResponse(status=http.HTTPStatus.UNAUTHORIZED, reason="You must be logged in to do that.")

    exhib = Exhibition.objects.get(id=exhibition_id)

    if not exhib.user == request.user:
        return HttpResponseForbidden(reason=FORBIDDEN_MSG)

    exhib.delete()

    messages.success(request, "Exhibition deleted successfully.")

    return HttpResponseRedirect("/gallery/exhibitions/")


# Form validation methods


def validate_gallery_piece_title(t):
    if len(t) > PIECE_TITLE_LEN_MAX:
        raise ValidationError("Title is too long (Max 500 characters)")

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
        raise ValidationError("File too large (Max 10 MB)")


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


def validate_exhibition_title(t):
    if not t:
        raise ValidationError("Title cannot be blank.")

    if len(t) > EXHIB_TITLE_LEN_MAX:
        raise ValidationError("Title is too long (Max 200 characters)")


def validate_exhibition_description(d):
    if len(d) > EXHIB_DESC_LEN_MAX:
        raise ValidationError("Description is too long (Max 1000 characters)")
