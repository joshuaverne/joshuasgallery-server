from django.urls import path

from . import views

urlpatterns = [
    # ex: /gallery/
    path('', views.index, name='index'),
    # ex: /gallery/exhib/5
    path('exhib/<int:exhibition_id>', views.exhibition_detail, name='exhibition_detail'),
    # ex: /gallery/piece/5
    path('piece/<int:piece_id>', views.piece_detail, name='piece_detail'),
    # ex: /gallery/add_gallery_piece
    path('add_gallery_piece', views.get_new_gallery_piece, name='get_new_gallery_piece')
]
