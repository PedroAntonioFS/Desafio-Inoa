from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import *
from .forms import *
from .facade import HttpFacade, B3Facade
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

    def post(self, request, *args, **kwargs):
        self._price = B3Facade.get_asset_price(request.POST['ticker'])

        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        
        kwargs = super().get_form_kwargs()

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({'price': self._price})

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['days'] = 0
        context['remain_time'] = "00:00:00"

        return context

    def form_valid(self, form):
        self.object = form.save(commit = False)
        user = User.objects.get(username="user1")
        
        self.object.investor = user
        self.object.price = self._price

        self.object.save()

        return HttpFacade.call_redirect(self.get_success_url())

class UpdateAssetView(UpdateView):
    template_name = 'core/asset/update.html'
    model = Asset
    form_class = AssetForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        self._price = B3Facade.get_asset_price(request.POST['ticker'])

        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        
        kwargs = super().get_form_kwargs()

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({'price': self._price})

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        days, remain_time = split_timedelta(self.object.sleep_time)
        context['days'] = days
        context['remain_time'] = remain_time

        return context

    def form_valid(self, form):
        self.object = form.save(commit = False)
        
        self.object.price = self._price

        self.object.save()

        return HttpFacade.call_redirect(self.get_success_url())

class DeleteAssetView(DeleteView):
    template_name = 'core/asset/delete.html'
    model = Asset
    success_url = '/'