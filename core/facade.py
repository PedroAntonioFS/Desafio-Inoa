from django.db import models
from django.core.exceptions import ValidationError

class ModelFacade:

    @staticmethod
    def create_ForeignKey(to):
        return models.ForeignKey(to, on_delete=models.CASCADE)

    @staticmethod
    def create_CharField(label, max_length):
        return models.CharField(label, max_length=max_length, blank=False)

    @staticmethod
    def create_MoneyField(label, max_digits):
        return models.DecimalField(label, max_digits=max_digits, decimal_places=2)

    @staticmethod
    def create_DurationField(label):
        return models.DurationField(label)

class DjangoExceptionsFacade:

    @staticmethod
    def raise_ValidationError(message):
            raise ValidationError(message)