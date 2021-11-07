from time import sleep
from django.conf import settings
from django.core.mail import send_mail
from .facade import B3Facade
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
        if price > 0:
            asset.price = price
            asset.save()
        
        asset = Asset.objects.get(id=asset.id)

class BaseAssetNotifier:
    _subject = None
    _message = None

    def __init__(self, asset, investor):
        self._asset = asset
        self._investor = investor

    def get_message(self):
        pass

    def send_email(self):
        send_mail(
            self._subject,
            self.get_message(),
            settings.EMAIL_HOST_USER,
            [self._investor.email,]
        )