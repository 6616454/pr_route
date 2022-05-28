from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator

from .models import City
from .forms import HtmlForm, CityForm


def home(request):
    cities = City.objects.all()
    pages = Paginator(cities, 2)
    page_number = request.GET.get('page')
    page_obj = pages.get_page(page_number)
    context = {
        'page_obg': page_obj
    }
    return render(request, 'cities/home.html', context=context)


class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/detail.html'


class CityCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy('cities:home')
    success_message = f'Город создан успешно!'


class CityUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    # success_url = reverse_lazy('cities:detail')
    success_message = f'Город отредактирован успешно!'


class CityDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = City
    template_name = 'cities/delete.html'
    success_url = reverse_lazy('cities:home')
    success_message = f'Город удалён успешно!'
