from datetime import timedelta
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from .facade import *
from .models import *
from .forms import *
from .templatetags.poll_extra import *

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

class TestAssetsListView(TestCase):
    def setUp(self):
        self._user = User.objects.create(username="user1")
        
        self._asset1 = Asset.objects.create(investor=self._user, name="PETR4", price=27.48, max_limit=50.00, min_limit=19.07, sleep_time=timedelta(days=1))
        self._asset2 = Asset.objects.create(investor=self._user, name="VALE3", price=71.96, max_limit=120.00, min_limit=50.00, sleep_time=timedelta(days=5))
        self._asset3 = Asset.objects.create(investor=self._user, name="GOLGL34", price=111.56, max_limit=170.00, min_limit=110.00, sleep_time=timedelta(days=7))

    def test_url(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get('')
        self.assertEqual(response.template_name[0], 'core/asset/list.html')

    def test_context(self):
        response = self.client.get('')

        self.assertEquals(response.context['object_list'][0], self._asset1)
        self.assertEquals(response.context['object_list'][1], self._asset2)
        self.assertEquals(response.context['object_list'][2], self._asset3)

class Test_poll_extra(TestCase):
    def format_timedelta_in_pt_br(self):
        hours12 = format_timedelta_in_pt_br(timedelta(hours=12))
        day1 = format_timedelta_in_pt_br(timedelta(days=1))
        day5 = format_timedelta_in_pt_br(timedelta(days=5))

        self.assertEquals(hours12, "12:00:00")
        self.assertEquals(day1, "1 dia, 00:00:00")
        self.assertEquals(day5, "5 dias, 00:00:00")

class TestAssetForm(TestCase):
    def test_add_asset(self):
        form = AssetForm({'name':"PETR4", 'max_limit':50.00, 'min_limit':19.07, 'sleep_time':timedelta(days=1)})
        self.assertTrue(form.is_valid())

    def test_min_bigger_than_max(self):
        form = AssetForm({'name':"PETR4", 'max_limit':19.07, 'min_limit':50.00, 'sleep_time':timedelta(days=1)})
        self.assertFalse(form.is_valid())

    def test_null_constraint(self):
        form = AssetForm({'name':None, 'max_limit':50.00, 'min_limit':19.07, 'sleep_time':timedelta(days=1)})
        self.assertFalse(form.is_valid())
        form = AssetForm({'name':"PETR4", 'max_limit':None, 'min_limit':19.07, 'sleep_time':timedelta(days=1)})
        self.assertFalse(form.is_valid())
        form = AssetForm({'name':"PETR4", 'max_limit':50.00, 'min_limit':None, 'sleep_time':timedelta(days=1)})
        self.assertFalse(form.is_valid())
        form = AssetForm({'name':"PETR4", 'max_limit':50.00, 'min_limit':19.07, 'sleep_time':None})
        self.assertFalse(form.is_valid())

class TestAddAssetView(TestCase):
    def setUp(self):
        self._user = User.objects.create(username="user1")

    def test_url(self):
        response = self.client.get('/add/')
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get('/add/')
        self.assertTemplateUsed(response, 'core/asset/add.html')

    def test_add_asset(self):
        sleep_time = timedelta(days=1)
        response = self.client.post('/add/', {'name':"PETR4", 'max_limit':50.00, 'min_limit':19.07, 'sleep_time':sleep_time}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/asset/list.html')

        asset = Asset.objects.get(name="PETR4", investor=self._user)

        self.assertIsNotNone(asset)
        self.assertEqual(asset.investor, self._user)
        self.assertEqual(asset.name, "PETR4")
        self.assertEqual(asset.price, Decimal('10.00'))
        self.assertEqual(asset.max_limit, Decimal('50.00'))
        self.assertEqual(asset.min_limit, Decimal('19.07'))
        self.assertEqual(asset.sleep_time, sleep_time)

    def test_min_bigger_than_max(self):
        self.client.post('/add/', {'name':"PETR4", 'max_limit':19.07, 'min_limit':50.00, 'sleep_time':timedelta(days=1)})

        try:
            Asset.objects.get(name="PETR4", investor=self._user)
            self.fail("Invalid: min_limit >= max_limit")
        except:
            pass

    def test_null_constraint(self):
        try:
            self.client.post('/add/', {'name':None, 'max_limit':50.00, 'min_limit':19.07, 'sleep_time':timedelta(days=1)})
            self.client.post('/add/', {'name':"PETR4", 'max_limit':None, 'min_limit':19.07, 'sleep_time':timedelta(days=1)})
            self.client.post('/add/', {'name':"PETR4", 'max_limit':50.00, 'min_limit':None, 'sleep_time':timedelta(days=1)})
            self.client.post('/add/', {'name':"PETR4", 'max_limit':50.00, 'min_limit':19.07, 'sleep_time':None})
            self.fail("Invalid: Not null constraint fail")
        except:
            pass

    def test_unique_constraint(self):
        try:
            sleep_time = timedelta(days=1)
            self.client.post('/add/', {'name':"PETR4", 'max_limit':50.00, 'min_limit':19.07, 'sleep_time':sleep_time}, follow=True)
            self.client.post('/add/', {'name':"PETR4", 'max_limit':50.00, 'min_limit':19.07, 'sleep_time':sleep_time}, follow=True)
            self.fail("Invalid: Unique constraint fail")
        except:
            pass

class TestUpdateAssetView(TestCase):
    def setUp(self):
        self._user = User.objects.create(username="user1")
        self._asset = Asset.objects.create(investor=self._user, name="PETR4", price=27.48, max_limit=50.00, min_limit=19.07, sleep_time=timedelta(days=1))

    def test_url(self):
        response = self.client.get('/{}/update/'.format(self._asset.id))
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get('/{}/update/'.format(self._asset.id))
        self.assertTemplateUsed(response, 'core/asset/update.html')
        
    def test_update_asset(self):
        sleep_time = timedelta(days=1)
        response = self.client.post('/{}/update/'.format(self._asset.id), {'name':"PETR4", 'max_limit':60.00, 'min_limit':20.00, 'sleep_time':sleep_time}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/asset/list.html')

        asset = Asset.objects.get(name="PETR4", investor=self._user)

        self.assertIsNotNone(asset)
        self.assertEqual(asset.investor, self._user)
        self.assertEqual(asset.name, "PETR4")
        self.assertEqual(asset.price, Decimal('10.00'))
        self.assertEqual(asset.max_limit, Decimal('60.00'))
        self.assertEqual(asset.min_limit, Decimal('20.00'))
        self.assertEqual(asset.sleep_time, sleep_time)
        
    def test_min_bigger_than_max(self):
        self.client.post('/{}/update/'.format(self._asset.id), {'name':"PETR4", 'max_limit':19.07, 'min_limit':50.00, 'sleep_time':timedelta(days=1)})

        try:
            Asset.objects.get(name="PETR4", investor=self._user)
            self.fail("Invalid: min_limit >= max_limit")
        except:
            pass
        
    def test_null_constraint(self):
        try:
            self.client.post('/{}/update/'.format(self._asset.id), {'name':None, 'max_limit':50.00, 'min_limit':19.07, 'sleep_time':timedelta(days=1)})
            self.client.post('/{}/update/'.format(self._asset.id), {'name':"PETR4", 'max_limit':None, 'min_limit':19.07, 'sleep_time':timedelta(days=1)})
            self.client.post('/{}/update/'.format(self._asset.id), {'name':"PETR4", 'max_limit':50.00, 'min_limit':None, 'sleep_time':timedelta(days=1)})
            self.client.post('/{}/update/'.format(self._asset.id), {'name':"PETR4", 'max_limit':50.00, 'min_limit':19.07, 'sleep_time':None})
            self.fail("Invalid: Not null constraint fail")
        except:
            pass

class TestUpdateAssetView(TestCase):
    def setUp(self):
        self._user = User.objects.create(username="user1")
        self._asset = Asset.objects.create(investor=self._user, name="PETR4", price=27.48, max_limit=50.00, min_limit=19.07, sleep_time=timedelta(days=1))

    def test_url(self):
        response = self.client.get('/{}/delete/'.format(self._asset.id))
        self.assertEqual(response.status_code, 200)
        
    def test_template(self):
        response = self.client.get('/{}/delete/'.format(self._asset.id))
        self.assertTemplateUsed(response, 'core/asset/delete.html')

    def test_update_asset(self):
        sleep_time = timedelta(days=1)
        response = self.client.post('/{}/delete/'.format(self._asset.id), {'name':"PETR4", 'max_limit':60.00, 'min_limit':20.00, 'sleep_time':sleep_time}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/asset/list.html')

        try:
            Asset.objects.get(name="PETR4", investor=self._user)
            self.fail("Invalid: Delete Asset fail")
        except:
            pass