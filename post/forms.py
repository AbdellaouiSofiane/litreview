from django import forms
from django.utils.safestring import mark_safe
from .models import Ticket, Review


def get_rating_choices():
    return [(i, str(i)) for i in range(6)]


class ImagePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs, **kwargs)
        img_html = mark_safe(f'<img src="{value.url}"/>') if value else ''
        return f'{img_html}{input_html}'


class ReviewForm(forms.ModelForm):
    rating = forms.TypedChoiceField(
        label='Note', choices=get_rating_choices,
        widget=forms.RadioSelect()
    )

    class Meta:
        model = Review
        fields = ['title', 'rating', 'description']


class TicketUpdateForm(forms.ModelForm):
    picture = forms.ImageField(
        label='Image', required=False, widget=ImagePreviewWidget
    )

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'picture']
