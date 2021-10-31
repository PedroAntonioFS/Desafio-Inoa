from django.test import TestCase
from django.contrib.auth.models import User
from .facade import *

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
