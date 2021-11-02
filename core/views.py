from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from .facade import HttpFacade

class AssetsListView(ListView):
    template_name = "core/asset/list.html"
    model = Asset

    def get_query_set(self):
        query = super().get_queryset()
        user = User.objects.get(username="user1")

        return query.filter(investor=user)

class AddAssetView(CreateView):
    template_name = "core/asset/add.html"
    form_class = AssetForm
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit = False)
        user = User.objects.get(username="user1")
        price = 10.00

        self.object.investor = user
        self.object.price = price

        self.object.save()

        return HttpFacade.call_redirect(self.get_success_url())