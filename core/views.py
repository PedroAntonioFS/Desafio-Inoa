from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from .models import *
from .forms import *
from .facade import HttpFacade
from .utils import *

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['days'] = 0
        context['remain_time'] = "00:00:00"

        return context

    def form_valid(self, form):
        self.object = form.save(commit = False)
        user = User.objects.get(username="user1")
        price = 10.00

        self.object.investor = user
        self.object.price = price

        self.object.save()

        return HttpFacade.call_redirect(self.get_success_url())

class UpdateAssetView(UpdateView):
    template_name = 'core/asset/update.html'
    model = Asset
    form_class = AssetForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        days, remain_time = split_timedelta(self.object.sleep_time)
        context['days'] = days
        context['remain_time'] = remain_time

        return context

    def form_valid(self, form):
        self.object = form.save(commit = False)
        price = 10.00
        
        self.object.price = price

        self.object.save()

        return HttpFacade.call_redirect(self.get_success_url())

