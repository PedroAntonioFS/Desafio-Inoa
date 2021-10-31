from django.urls import path, include
from .views import *

urlpatterns = [
    path('', AssetsListView.as_view())
]