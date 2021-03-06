from datetime import timedelta
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .facade import *
from .models import *
from .forms import *
from .templatetags.poll_extra import *
from .utils import *
from .constants import *

class TestModelFacade(TestCase):

    def test_create_ForeignKey(self):
        field = ModelFacade.create_ForeignKey(User)
        self.assertEqual(field.related_model, User)

    def test_create_CharField(self):
        field = ModelFacade.create_CharField('teste', 30)
        self.assertEqual(field.verbose_name, 'teste')
        self.assertEqual(field.max_length, 30)

    def test_create_MoneyField(self):
        field = ModelFacade.create_MoneyField('teste', 16)
        self.assertEqual(field.verbose_name, 'teste')
        self.assertEqual(field.max_digits, 16)
        self.assertEqual(field.decimal_places, 2)

    def test_create_DurationField(self):
        field = ModelFacade.create_DurationField('teste')
        self.assertEqual(field.verbose_name, 'teste')

class TestFormFacade(TestCase):

    def test_create_email_field(self):
        field = FormFacade.create_EmailField(required=True)
        self.assertEqual(field.label, 'Email')
        self.assertTrue(field.required)

class TestAsset(TestCase):
    def setUp(self):
        self._user = User.objects.create(username="user1")

    def test_create_Asset(self):
        sleep_time = timedelta(days=1)
        asset = Asset.objects.create(investor=self._user, ticker="PETR4", price=27.48, max_limit=19.07, min_limit=50.00, sleep_time=sleep_time)
        
        self.assertEqual(asset.investor, self._user)
        self.assertEqual(asset.ticker, "PETR4")
        self.assertEqual(asset.price, 27.48)
        self.assertEqual(asset.max_limit, 19.07)
        self.assertEqual(asset.min_limit, 50.00)
        self.assertEqual(asset.sleep_time, sleep_time)

    def test_null_constraint(self):
        sleep_time = timedelta(days=1)
        try:
            Asset.objects.create(investor=None, ticker="PETR4", price=27.48, max_limit=19.07, min_limit=50.00, sleep_time=sleep_time)
            self.fail("Null constraint fail!")
        except:
            pass
        try:
            Asset.objects.create(investor=self._user, ticker=None, price=27.48, max_limit=19.07, min_limit=50.00, sleep_time=sleep_time)
            self.fail("Null constraint fail!")
        except:
            pass
        try:
            Asset.objects.create(investor=self._user, ticker="PETR4", price=None, max_limit=19.07, min_limit=50.00, sleep_time=sleep_time)
            self.fail("Null constraint fail!")
        except:
            pass
        try:
            Asset.objects.create(investor=self._user, ticker="PETR4", price=27.48, max_limit=None, min_limit=50.00, sleep_time=sleep_time)
            self.fail("Null constraint fail!")
        except:
            pass
        try:
            Asset.objects.create(investor=self._user, ticker="PETR4", price=27.48, max_limit=19.07, min_limit=None, sleep_time=sleep_time)
            self.fail("Null constraint fail!")
        except:
            pass
        try:
            Asset.objects.create(investor=self._user, ticker="PETR4", price=27.48, max_limit=19.07, min_limit=50.00, sleep_time=None)
            self.fail("Null constraint fail!")
        except:
            pass

    def test_unique_constraint(self):
        sleep_time = timedelta(days=1)
        try:
            Asset.objects.create(investor=self._user, ticker="PETR4", price=27.48, max_limit=19.07, min_limit=50.00, sleep_time=sleep_time)
            Asset.objects.create(investor=self._user, ticker="PETR4", price=27.48, max_limit=19.07, min_limit=50.00, sleep_time=sleep_time)
            self.fail("Unique constraint fail!")
        except:
            pass

class TestAssetsListView(TestCase):
    def setUp(self):
        form = UserCreationForm({'username': 'user1', 'password1': 'Senha1234', 'password2': 'Senha1234'})
        form.save()
        form = UserCreationForm({'username': 'user2', 'password1': 'Senha1234', 'password2': 'Senha1234'})
        form.save()
        self._user = User.objects.get(username="user1")
        user2 = User.objects.get(username="user2")
        
        self._asset1 = Asset.objects.create(investor=self._user, ticker="PETR4", price=27.48, max_limit=50.00, min_limit=19.07, sleep_time=timedelta(days=1))
        self._asset2 = Asset.objects.create(investor=self._user, ticker="VALE3", price=71.96, max_limit=120.00, min_limit=50.00, sleep_time=timedelta(days=5))
        self._asset3 = Asset.objects.create(investor=self._user, ticker="GOLGL34", price=111.56, max_limit=170.00, min_limit=110.00, sleep_time=timedelta(days=7))
        self._asset4 = Asset.objects.create(investor=user2, ticker="TSLA34", price=175.21, max_limit=200.00, min_limit=110.00, sleep_time=timedelta(days=7))

        self.client.post('/accounts/login/', {'username':'user1', 'password': 'Senha1234'})

    def test_url(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'core/asset/list.html')

    def test_context(self):
        response = self.client.get('')

        self.assertEqual(len(response.context['object_list']), 3)
        self.assertEqual(response.context['object_list'][0], self._asset1)
        self.assertEqual(response.context['object_list'][1], self._asset2)
        self.assertEqual(response.context['object_list'][2], self._asset3)

class TestPollExtra(TestCase):
    def format_timedelta_in_pt_br(self):
        hours12 = format_timedelta_in_pt_br(timedelta(hours=12))
        day1 = format_timedelta_in_pt_br(timedelta(days=1))
        day5 = format_timedelta_in_pt_br(timedelta(days=5))

        self.assertEqual(hours12, "12:00:00")
        self.assertEqual(day1, "1 dia, 00:00:00")
        self.assertEqual(day5, "5 dias, 00:00:00")

class TestAssetForm(TestCase):
    def test_add_asset(self):
        form = AssetForm({'ticker':"PETR4", 'max_limit':50.00, 'min_limit':19.07, 'sleep_time':timedelta(days=1)})
        self.assertTrue(form.is_valid())

    def test_min_bigger_than_max(self):
        form = AssetForm({'ticker':"PETR4", 'max_limit':19.07, 'min_limit':50.00, 'sleep_time':timedelta(days=1)})
        self.assertFalse(form.is_valid())

    def test_null_constraint(self):
        form = AssetForm({'ticker':None, 'max_limit':50.00, 'min_limit':19.07, 'sleep_time':timedelta(days=1)})
        self.assertFalse(form.is_valid())
        form = AssetForm({'ticker':"PETR4", 'max_limit':None, 'min_limit':19.07, 'sleep_time':timedelta(days=1)})
        self.assertFalse(form.is_valid())
        form = AssetForm({'ticker':"PETR4", 'max_limit':50.00, 'min_limit':None, 'sleep_time':timedelta(days=1)})
        self.assertFalse(form.is_valid())
        form = AssetForm({'ticker':"PETR4", 'max_limit':50.00, 'min_limit':19.07, 'sleep_time':None})
        self.assertFalse(form.is_valid())

    def test_negative(self):
        form = AssetForm({'ticker':"PETR4", 'max_limit':-50.00, 'min_limit':19.07, 'sleep_time':timedelta(days=1)})
        self.assertFalse(form.is_valid())

    def test_not_found_error(self):
        form = AssetForm({'ticker':"PETR4", 'max_limit':-50.00, 'min_limit':19.07, 'sleep_time':timedelta(days=1)}, price=ASSET_NOT_FOUND_ERROR)
        self.assertFalse(form.is_valid())

    def test_request_limit_error(self):
        form = AssetForm({'ticker':"PETR4", 'max_limit':50.00, 'min_limit':19.07, 'sleep_time':timedelta(days=1)}, price=API_REQUEST_LIMIT_ERROR)
        self.assertFalse(form.is_valid())

class TestAddAssetView(TestCase):
    def setUp(self):
        form = UserCreationForm({'username': 'user1', 'password1': 'Senha1234', 'password2': 'Senha1234'})
        form.save()
        self._user = User.objects.get(username="user1")
        self.client.post('/accounts/login/', {'username':'user1', 'password': 'Senha1234'})

    def test_url(self):
        response = self.client.get('/add/')
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get('/add/')
        self.assertTemplateUsed(response, 'core/asset/add.html')

    def test_add_asset(self):
        sleep_time = timedelta(days=1)
        response = self.client.post('/add/', {'ticker':"PETR4", 'max_limit':50.00, 'min_limit':19.07, 'sleep_time':sleep_time}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/asset/list.html')

        asset = Asset.objects.get(ticker="PETR4", investor=self._user)

        self.assertIsNotNone(asset)
        self.assertEqual(asset.investor, self._user)
        self.assertEqual(asset.ticker, "PETR4")
        self.assertEqual(type(asset.price), type(Decimal('10.00')))
        self.assertEqual(asset.max_limit, Decimal('50.00'))
        self.assertEqual(asset.min_limit, Decimal('19.07'))
        self.assertEqual(asset.sleep_time, sleep_time)

    def test_not_found(self):
        sleep_time = timedelta(days=1)
        self.client.post('/add/', {'ticker':"TESTE", 'max_limit':50.00, 'min_limit':19.07, 'sleep_time':sleep_time}, follow=True)
        
        try:
            Asset.objects.get(ticker="TESTE", investor=self._user)
            self.fail('Invalid: Asset does not exists error was not raised!')
        except:
            pass

class TestUpdateAssetView(TestCase):
    def setUp(self):
        form = UserCreationForm({'username': 'user1', 'password1': 'Senha1234', 'password2': 'Senha1234'})
        form.save()
        self._user = User.objects.get(username="user1")
        self.client.post('/accounts/login/', {'username':'user1', 'password': 'Senha1234'})

        self._asset = Asset.objects.create(investor=self._user, ticker="PETR4", price=27.48, max_limit=50.00, min_limit=19.07, sleep_time=timedelta(days=1))

    def test_url(self):
        response = self.client.get('/{}/update/'.format(self._asset.id))
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get('/{}/update/'.format(self._asset.id))
        self.assertTemplateUsed(response, 'core/asset/update.html')
        
    def test_update_asset(self):
        sleep_time = timedelta(days=1)
        response = self.client.post('/{}/update/'.format(self._asset.id), {'ticker':"PETR4", 'max_limit':60.00, 'min_limit':20.00, 'sleep_time':sleep_time}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/asset/list.html')

        asset = Asset.objects.get(ticker="PETR4", investor=self._user)

        self.assertIsNotNone(asset)
        self.assertEqual(asset.investor, self._user)
        self.assertEqual(asset.ticker, "PETR4")
        self.assertEqual(type(asset.price), type(Decimal('10.00')))
        self.assertEqual(asset.max_limit, Decimal('60.00'))
        self.assertEqual(asset.min_limit, Decimal('20.00'))
        self.assertEqual(asset.sleep_time, sleep_time)

    def test_not_found(self):
        sleep_time = timedelta(days=1)
        self.client.post('/update/', {'ticker':"TESTE", 'max_limit':50.00, 'min_limit':19.07, 'sleep_time':sleep_time}, follow=True)
        
        try:
            Asset.objects.get(ticker="TESTE", investor=self._user)
            self.fail('Invalid: Asset does not exists error was not raised!')
        except:
            pass

class TestDeleteAssetView(TestCase):
    def setUp(self):
        form = UserCreationForm({'username': 'user1', 'password1': 'Senha1234', 'password2': 'Senha1234'})
        form.save()
        self._user = User.objects.get(username="user1")
        self.client.post('/accounts/login/', {'username':'user1', 'password': 'Senha1234'})

        self._asset = Asset.objects.create(investor=self._user, ticker="PETR4", price=27.48, max_limit=50.00, min_limit=19.07, sleep_time=timedelta(days=1))

    def test_url(self):
        response = self.client.get('/{}/delete/'.format(self._asset.id))
        self.assertEqual(response.status_code, 200)
        
    def test_template(self):
        response = self.client.get('/{}/delete/'.format(self._asset.id))
        self.assertTemplateUsed(response, 'core/asset/delete.html')

    def test_delete_asset(self):
        sleep_time = timedelta(days=1)
        response = self.client.post('/{}/delete/'.format(self._asset.id), {'ticker':"PETR4", 'max_limit':60.00, 'min_limit':20.00, 'sleep_time':sleep_time}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/asset/list.html')

        try:
            Asset.objects.get(ticker="PETR4", investor=self._user)
            self.fail("Invalid: Delete Asset fail")
        except:
            pass

class TestB3Facade(TestCase):
    def test_get_asset_price(self):
        petr4 = B3Facade.get_asset_price("PETR4")
        self.assertIsNotNone(petr4)

class TestAuthentication(TestCase):
    def setUp(self):
        form = UserCreationForm({'username': 'user1', 'password1': 'Senha1234', 'password2': 'Senha1234'})
        form.save()

    def test_url(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get('/accounts/login/')
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login(self):
        response = self.client.post('/accounts/login/', {'username': 'user1', 'password': 'Senha1234'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.wsgi_request.user.username, 'user1')

    def test_logout(self):
        self.client.post('/accounts/login/', {'username': 'user1', 'password': 'Senha1234'})
        response = self.client.get('/accounts/logout/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.wsgi_request.user.username, 'user1')
        self.assertTemplateUsed('registration/login.html')

    def test_login_required(self):
        response = self.client.get('', follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')

        response = self.client.get('/add/', follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')
        
        self._user = User.objects.get(username="user1")
        self._asset = Asset.objects.create(investor=self._user, ticker="PETR4", price=27.48, max_limit=50.00, min_limit=19.07, sleep_time=timedelta(days=1))

        response = self.client.get('/{}/update/'.format(self._asset.id), follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')

        response = self.client.get('/{}/delete/'.format(self._asset.id), follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')

class TestCreateUserView(TestCase):
    def test_url(self):
        response = self.client.get('/sign_up/')
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get('/sign_up/')
        self.assertTemplateUsed(response, 'core/sign_up.html')

    def test_create_user(self):
        self.client.post('/sign_up/', {'username': 'user1', 'password1': 'Senha1234', 'password2': 'Senha1234', 'email': 'teste@teste.com'})

        try:
            user = User.objects.get(username='user1')
        except:
            self.fail('Invalid: User was not saved!')

        self.assertEqual(user.username, 'user1')