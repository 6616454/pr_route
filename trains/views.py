from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator

from .models import Train
# from .forms import HtmlForm, TrainForm
from .forms import TrainForm


def home(request):
    if request.method == 'POST':
        form = TrainForm(request.POST)
        if form.is_valid():
            cf = form.cleaned_data
            Train.objects.create(
                name=cf['name']
            )

    form = TrainForm()
    trains = Train.objects.all()
    pages = Paginator(trains, 2)
    page_number = request.GET.get('page')
    page_obj = pages.get_page(page_number)
    context = {
        'trains': trains,
        'form': form,
        'page_obg': page_obj
    }
    return render(request, 'trains/home.html', context=context)


class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    template_name = 'trains/detail.html'


class TrainCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/create.html'
    success_url = reverse_lazy('trains:home')
    success_message = f'Поезд создан успешно!'


class TrainUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/update.html'
    success_message = f'Поезд отредактирован успешно!'


class TrainDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Train
    template_name = 'trains/delete.html'
    success_url = reverse_lazy('trains:home')
    success_message = f'Поезд удалён успешно!'
