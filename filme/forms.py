from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django import forms

class CriarContaForm(UserCreationForm):
    email = forms.EmailField()

    #a função usuario personalizada que criamos na view
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')


class FormHomepage(forms.Form):
    email = forms.EmailField(label=False)