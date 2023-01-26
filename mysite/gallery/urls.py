from django.urls import path

from . import views

urlpatterns = [
    # ex: /gallery/
    path('', views.index, name='index'),
    # ex: /gallery/exhib/5
    path('exhib/<int:exhibition_id>', views.exhibition_detail, name='exhibition_detail'),
    # ex: /gallery/piece/5
    path('piece/<int:piece_id>', views.piece_detail, name='piece_detail')

]