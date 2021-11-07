from django.apps import AppConfig
from threading import Thread
from .facade import B3Facade
import os

teste = True
class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            super().ready()
            from .models import Asset
            from .utils import timed_asset_update

            assets_list = Asset.objects.all()

            for asset in assets_list:
                thread = Thread(target=timed_asset_update, args=(asset, ))
                thread.daemon = True
                thread.start()
