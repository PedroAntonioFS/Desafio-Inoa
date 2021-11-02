from django.urls import path, include
from .views import *

urlpatterns = [
    path('', AssetsListView.as_view(), name="home"),
    path('add/', AddAssetView.as_view(), name="add_asset")
]