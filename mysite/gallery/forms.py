from django import forms
from models import GalleryPiece


class NewGalleryPieceForm(forms.Form):
    title = forms.CharField(label='Title', max_length=500)
    description = forms.CharField(label='Description', max_length=1000)

