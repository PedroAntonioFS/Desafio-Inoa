from django.db import models
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from urllib import request
import json
from .constants import ASSET_NOT_FOUND_ERROR, API_REQUEST_LIMIT_ERROR

def validate_negative(value):
    if value < 0:
        DjangoExceptionsFacade.raise_ValidationError("Valor Inválido: {}. O campo não pode ser negativo".format(value))

class ModelFacade:

    @staticmethod
    def create_ForeignKey(to):
        return models.ForeignKey(to, on_delete=models.CASCADE)

    @staticmethod
    def create_CharField(label, max_length):
        return models.CharField(label, max_length=max_length, blank=False)

    @staticmethod
    def create_MoneyField(label, max_digits):
        return models.DecimalField(label, max_digits=max_digits, decimal_places=2, validators=[validate_negative])

    @staticmethod
    def create_DurationField(label):
        return models.DurationField(label)

class DjangoExceptionsFacade:

    @staticmethod
    def raise_ValidationError(message):
            raise ValidationError(message)

class HttpFacade:

    @staticmethod
    def call_redirect(url):
        return HttpResponseRedirect(url)

class B3Facade:

    @staticmethod
    def get_asset_price(asset):
        url = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={}.SA&apikey=KOLIMB2YNWG6T5QI".format(asset)
        
        with request.urlopen(url) as response:
            data = response.read()

        try:
            price = float(json.loads(data.decode('utf-8'))['Global Quote']['05. price'])
        except:
            try:
                json.loads(data.decode('utf-8'))['Global Quote']
                price = ASSET_NOT_FOUND_ERROR
            except:
                price = API_REQUEST_LIMIT_ERROR
        finally:
            return price