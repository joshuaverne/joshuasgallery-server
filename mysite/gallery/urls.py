from django.urls import path

from . import views

urlpatterns = [
    # ex: /gallery/
    path('', views.index, name='index'),

    # ex: /gallery/pieces
    path('pieces/', views.pieces_list_view, name='pieces_list_view'),

    # ex: /gallery/pieces/5
    path('pieces/<int:piece_id>/', views.piece_detail, name='piece_detail'),

    # ec: /gallery/pieces/new
    path('pieces/new/', views.new_gallery_piece, name='piece_new'),

    # ex: /gallery/pieces/5/edit
    path('pieces/<int:piece_id>/edit/', views.edit_gallery_piece, name='piece_edit'),

    # ex: /gallery/exhibitions
    path('exhibitions/', views.exhibitions_list_view, name='exhibitions_list_view'),

    # ex: /gallery/exhib/5
    path('exhib/<int:exhibition_id>/', views.exhibition_detail, name='exhibition_detail'),

    # ex: /gallery/add-gallery-piece
    path('add-gallery-piece/', views.get_new_gallery_piece, name='get_new_gallery_piece'),

    # ex: /gallery/add-exhibition
    path('add-exhibition/', views.get_new_exhibition, name='get_new_exhibition')
]
