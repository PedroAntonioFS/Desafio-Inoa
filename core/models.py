from django.db import models
from django.contrib.auth.models import User
from .facade import ModelFacade, B3Facade

class Asset(models.Model):
    investor = ModelFacade.create_ForeignKey(User)
    name = ModelFacade.create_CharField("Ativo", 10)
    price = ModelFacade.create_MoneyField("Preço", 5)
    max_limit = ModelFacade.create_MoneyField("Limite máximo", 5)
    min_limit = ModelFacade.create_MoneyField("Limite mínimo", 5)
    sleep_time = ModelFacade.create_DurationField("Periodicidade de atualização")

    class Meta:
        verbose_name = "Ativo"
        unique_together = ['investor', 'name']