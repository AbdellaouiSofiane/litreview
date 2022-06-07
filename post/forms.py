from tabnanny import verbose
from django import forms
from .models import Review


def get_rating_choices():
    return [(i, str(i)) for i in range(6)]

class ReviewForm(forms.ModelForm):
    rating = forms.TypedChoiceField(
        label='Note',
        choices=get_rating_choices,
        widget=forms.RadioSelect()
    )

    class Meta:
        model = Review
        fields = ['title', 'rating', 'description']