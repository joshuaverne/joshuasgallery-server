from django import forms


class NewGalleryPieceForm(forms.Form):
    title = forms.CharField(label='Title', max_length=500, required=False)
    description = forms.CharField(label='Description', max_length=1000, required=False)
