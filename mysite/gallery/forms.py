from django import forms
from models import GalleryPiece


class NewGalleryPieceForm(forms.ModelForm):
    title = forms.CharField(required=True)

    class Meta:
        model = GalleryPiece
        fields = "title"

