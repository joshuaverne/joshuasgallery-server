from django.shortcuts import render
from django.http import HttpResponse

from .models import GalleryPiece, Exhibition


def index(request):
    exhibition_list = Exhibition.objects.all()
    pieces_list = GalleryPiece.objects.all()
    output = ', '.join([e.name for e in exhibition_list])
    output += ', '.join(p.title for p in pieces_list)
    return HttpResponse(output)


def exhibition_detail(request, exhibition_id):
    return HttpResponse("You're looking at exhibition %s." % exhibition_id)


def piece_detail(request, piece_id):
    return HttpResponse("You're looking at piece %s." % piece_id)
