from django.forms import ModelForm
from .models import *
from .facade import DjangoExceptionsFacade
from .utils import ASSET_NOT_FOUND_ERROR, API_REQUEST_LIMIT_ERROR

class AssetForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self._price = kwargs.pop('price', None)
        super().__init__(*args, **kwargs)
    class Meta:
        model = Asset
        fields = "__all__"
        exclude = ['investor', 'price']
    
    def clean(self):
        cleanedData = super().clean()

        min_limit = cleanedData.get('min_limit')
        max_limit = cleanedData.get('max_limit')
        
        if min_limit and max_limit and (min_limit >= max_limit):
            DjangoExceptionsFacade.raise_ValidationError("Limite mínimo deve ser menor que o limite máximo!")

        if self._price == ASSET_NOT_FOUND_ERROR:
            DjangoExceptionsFacade.raise_ValidationError("Ativo não encontrado!")

        if self._price == API_REQUEST_LIMIT_ERROR:
            DjangoExceptionsFacade.raise_ValidationError("O limite máximo de solicitações alcançado. A frequência permitida é de 5 chamadas por minuto e 500 chamadas por dia!")
