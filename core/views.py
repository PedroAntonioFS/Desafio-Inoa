from django.contrib.auth.models import User
from django.views.generic.list import ListView
from .models import *

class AssetsListView(ListView):
    template_name = "asset/list.html"
    model = Asset

    def get_query_set(self):
        query = super().get_queryset()
        user = User.objects.get(username="User1")

        return query.filter(investor=user)