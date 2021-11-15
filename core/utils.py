from time import sleep
from django.conf import settings
from .facade import B3Facade, MailFacade, ModelFacade
from .models import Asset

def split_timedelta(timedelta):
    seconds = timedelta.total_seconds()
    days = int(seconds // (60 * 60 * 24))

    seconds = seconds % (60 * 60 * 24)
    hours = int(seconds // (60 * 60))

    seconds = seconds % (60 * 60)
    minutes = int(seconds // 60)

    seconds = int(seconds % 60)

    hours_str = "0{}".format(hours)[-2:]
    minutes_str = "0{}".format(minutes)[-2:]
    seconds_str = "0{}".format(seconds)[-2:]

    return days, "{}:{}:{}".format(hours_str, minutes_str, seconds_str)

def timed_asset_update(asset):
    while True:
        sleep(asset.sleep_time.total_seconds())
        price = B3Facade.get_asset_price(asset.ticker)
        asset = ModelFacade.get_object(Asset, id=asset.id)
        if price > 0:
            asset.price = price
            asset.save()

        if price > asset.max_limit:
            sell = SellAssetNotifier(asset)
            sell.send_email()

        if price < asset.min_limit:
            sell = BuyAssetNotifier(asset)
            sell.send_email()

class BaseAssetNotifier:
    _subject = None
    _message = None

    def __init__(self, asset):
        self._asset = asset
        self._investor = asset.investor

    def get_message(self):
        pass

    def send_email(self):
        MailFacade.call_send_mail(
            self._subject,
            self.get_message(),
            settings.EMAIL_HOST_USER,
            [self._investor.email,]
        )

class SellAssetNotifier(BaseAssetNotifier):
    _subject = "Sugestão de venda da PETR4"
    _message = "Sr. Ou Sra. {}, o ativo PETR4 chegou ao limite máximo especificado.\nDados do Ativo {}:\nPreço: {} R$\nLimite máximo: {} R$"

    def get_message(self):
        return self._message.format(self._investor.first_name, self._asset.ticker, self._asset.price, self._asset.max_limit)
        
class BuyAssetNotifier(BaseAssetNotifier):
    _subject = "Sugestão de compra da PETR4"
    _message = "Sr. Ou Sra. {}, o ativo PETR4 chegou ao limite mínimo especificado.\nDados do Ativo {}:\nPreço: {} R$\nLimite mínimo: {} R$"

    def get_message(self):
        return self._message.format(self._investor.first_name, self._asset.ticker, self._asset.price, self._asset.min_limit)