from django import forms
from .models import UserFollows
from django.contrib.auth import get_user_model


class SubscriptionForm(forms.ModelForm):
    followed_user = forms.CharField(
        max_length=250,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Nom d'utilisateur"
        })
    )
    
    class Meta:
        model = UserFollows
        fields = ['followed_user',]

    def clean_followed_user(self):
        username = self.cleaned_data.get('followed_user')
        followed_user =  get_user_model().objects.filter(username=username)
        if not followed_user.exists():
            raise forms.ValidationError("Aucun utilisateur avec ce nom n'a été trouvé.")
        return followed_user.get()
