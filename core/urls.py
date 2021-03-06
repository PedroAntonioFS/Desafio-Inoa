from django.urls import path
from .views import *

urlpatterns = [
    path('', AssetsListView.as_view(), name="home"),
    path('add/', AddAssetView.as_view(), name="add_asset"),
    path('<pk>/update/', UpdateAssetView.as_view(), name="update_asset"),
    path('<pk>/delete/', DeleteAssetView.as_view(), name="delete_asset"),
    path('sign_up/', CreateUserView.as_view(), name="sign_up")
]