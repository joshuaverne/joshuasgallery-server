from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

from .models import GalleryPiece, Exhibition
from .forms import NewGalleryPieceForm


def index(request):
    exhibition_list = Exhibition.objects.all()
    pieces_list = GalleryPiece.objects.all()
    output = ', '.join([e.name for e in exhibition_list])
    output += ', '.join(p.title for p in pieces_list)
    return render(request=request, template_name="mysite/my_gallery_dashboard.html")


def exhibition_detail(request, exhibition_id):
    return HttpResponse("You're looking at exhibition %s." % exhibition_id)


def piece_detail(request, piece_id):
    return HttpResponse("You're looking at piece %s." % piece_id)


def get_new_gallery_piece(request):
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to do that.")

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewGalleryPieceForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # TODO: create the new GalleryPiece, add it to the database
            new_gallery_piece = GalleryPiece(title=form.cleaned_data.get(key="title"),
                                             pub_date=timezone.now(),
                                             user=request.user)
            new_gallery_piece.save()

            # redirect to a new URL:
            return HttpResponse("New Piece Saved Successfully.")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewGalleryPieceForm()

    return render(request, 'name.html', {'form': form})
