from datetime import timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from .facade import *
from .models import Asset

# Create your tests here.

class TestModelFacade(TestCase):

    def test_create_ForeignKey(self):
        field = ModelFacade.create_ForeignKey(User)
        self.assertEquals(field.related_model, User)

    def test_create_CharField(self):
        field = ModelFacade.create_CharField('teste', 30)
        self.assertEquals(field.verbose_name, 'teste')
        self.assertEquals(field.max_length, 30)

    def test_create_MoneyField(self):
        field = ModelFacade.create_MoneyField('teste', 16)
        self.assertEquals(field.verbose_name, 'teste')
        self.assertEquals(field.max_digits, 16)
        self.assertEquals(field.decimal_places, 2)

    def test_create_DurationField(self):
        field = ModelFacade.create_DurationField('teste')
        self.assertEquals(field.verbose_name, 'teste')

class TestAsset(TestCase):
    def setUp(self):
        self.teste = 1
        self._user = User.objects.create(username="user1")

    def test_create_Asset(self):
        sleep_time = timedelta(days=1)
        asset = Asset.objects.create(investor=self._user, name="PETR4", price=27.48, max_limit=19.07, min_limit=50.00, sleep_time=sleep_time)
        
        self.assertEquals(asset.investor, self._user)
        self.assertEquals(asset.name, "PETR4")
        self.assertEquals(asset.price, 27.48)
        self.assertEquals(asset.max_limit, 19.07)
        self.assertEquals(asset.min_limit, 50.00)
        self.assertEquals(asset.sleep_time, sleep_time)

    def test_null_constraint(self):
        sleep_time = timedelta(days=1)
        try:
            asset = Asset.objects.create(investor=None, name="PETR4", price=27.48, max_limit=19.07, min_limit=50.00, sleep_time=sleep_time)
            asset = Asset.objects.create(investor=self._user, name=None, price=27.48, max_limit=19.07, min_limit=50.00, sleep_time=sleep_time)
            asset = Asset.objects.create(investor=self._user, name="PETR4", price=None, max_limit=19.07, min_limit=50.00, sleep_time=sleep_time)
            asset = Asset.objects.create(investor=self._user, name="PETR4", price=27.48, max_limit=None, min_limit=50.00, sleep_time=sleep_time)
            asset = Asset.objects.create(investor=self._user, name="PETR4", price=27.48, max_limit=19.07, min_limit=None, sleep_time=sleep_time)
            asset = Asset.objects.create(investor=self._user, name="PETR4", price=27.48, max_limit=19.07, min_limit=50.00, sleep_time=None)
        except:
            pass

    def test_unique_constraint(self):
        sleep_time = timedelta(days=1)
        try:
            asset = Asset.objects.create(investor=self._user, name="PETR4", price=27.48, max_limit=19.07, min_limit=50.00, sleep_time=sleep_time)
            asset = Asset.objects.create(investor=self._user, name="PETR4", price=27.48, max_limit=19.07, min_limit=50.00, sleep_time=sleep_time)
        except:
            pass