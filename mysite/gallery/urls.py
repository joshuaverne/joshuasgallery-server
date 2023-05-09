from django.urls import path

from . import views

urlpatterns = [
    # ex: /gallery/
    path('', views.index, name='index'),

    # ex: /gallery/pieces
    path('pieces/', views.pieces_list_view, name='pieces_list_view'),

    # ec: /gallery/pieces/new
    path('pieces/new/', views.new_gallery_piece, name='piece_new'),

    # ex: /gallery/pieces/5
    path('pieces/<int:piece_id>/', views.piece_detail, name='piece_detail'),

    # ex: /gallery/pieces/5/edit
    path('pieces/<int:piece_id>/edit/', views.edit_gallery_piece, name='piece_edit'),

    # ex: /gallery/pieces/5/delete
    path('pieces/<int:piece_id>/delete/', views.delete_gallery_piece, name='piece_delete'),

    # ex: /gallery/exhibitions
    path('exhibitions/', views.exhibitions_list_view, name='exhibitions_list_view'),

    # ex: /gallery/exhibitions/new
    path('exhibitions/new/', views.new_exhibition, name='exhibition_new'),

    # ex: /gallery/exhibitions/5
    path('exhibitions/<int:exhibition_id>/', views.exhibition_detail, name='exhibition_detail'),
]
