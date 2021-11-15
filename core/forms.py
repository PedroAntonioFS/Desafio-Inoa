from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .facade import DjangoExceptionsFacade, FormFacade
from .constants import ASSET_NOT_FOUND_ERROR, API_REQUEST_LIMIT_ERROR

class AssetForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self._price = kwargs.pop('price', None)
        super().__init__(*args, **kwargs)
    class Meta:
        model = Asset
        fields = "__all__"
        exclude = ['investor', 'price']
    
    def clean(self):
        cleaned_data = super().clean()

        min_limit = cleaned_data.get('min_limit')
        max_limit = cleaned_data.get('max_limit')
        
        if min_limit and max_limit and (min_limit >= max_limit):
            DjangoExceptionsFacade.raise_ValidationError("Limite mínimo deve ser menor que o limite máximo!")

        if self._price == ASSET_NOT_FOUND_ERROR:
            DjangoExceptionsFacade.raise_ValidationError("Ativo não encontrado!")

        if self._price == API_REQUEST_LIMIT_ERROR:
            DjangoExceptionsFacade.raise_ValidationError("O limite máximo de solicitações alcançado. A frequência permitida é de 5 chamadas por minuto e 500 chamadas por dia!")

class CustomUserCreationForm(UserCreationForm):
    email = FormFacade.create_EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
