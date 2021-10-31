from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import *
from .facade import DjangoExceptionsFacade

class AssetForm(ModelForm):
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