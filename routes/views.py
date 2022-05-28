from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView

from cities.models import City
from routes.forms import RouteForm, AddRouteForm
from routes.models import Route
from routes.services import get_routes
from trains.models import Train


def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})


def route_list(request):
    routes = Route.objects.all()
    pages = Paginator(routes, 2)
    page_number = request.GET.get('page')
    page_obj = pages.get_page(page_number)
    context = {
        'page_obg': page_obj
    }
    return render(request, 'routes/list.html', context=context)


class RouteDetailView(DetailView):
    queryset = Route.objects.all()
    template_name = 'routes/detail.html'


def find_routes(request):
    if request.method == "POST":
        form = RouteForm(request.POST)
        if form.is_valid():
            try:
                context = get_routes(request, form)
            except ValueError as e:
                messages.error(request, e)
                return render(request, 'routes/home.html', {'form': form})
            return render(request, 'routes/home.html', context)
        return render(request, 'routes/home.html', {'form': form})
    else:
        form = RouteForm()
        messages.error(request, 'Нет данных для поиска')
        return render(request, 'routes/home.html', {'form': form})


def add_routes(request):
    if request.method == 'POST':
        context = {}
        data = request.POST  # данные с хидден полей
        if data:
            total_time = int(data['all_time'])
            from_city_id = int(data['from_city'])
            to_city_id = int(data['to_city'])
            trains = data['trains'].split(',')
            trains_list = [int(t) for t in trains if t.isdigit()]

            queryset = Train.objects.filter(id__in=trains_list).select_related('to_city', 'from_city')

            cities = City.objects.filter(id__in=[from_city_id,
                                                 to_city_id]).in_bulk()  # из queryset(список) в словарь(ключ id города: значение City экземпляр
            form = AddRouteForm(
                initial={
                    'from_city': cities[from_city_id],
                    'to_city': cities[to_city_id],
                    'all_time': total_time,
                    'trains': queryset
                }
            )
            context['form'] = form
        return render(request, 'routes/create.html', context)
    else:
        messages.error(request, "Невозможно сохранить несуществующий маршрут")
        return redirect('home')


def save_routes(request):
    if request.method == 'POST':
        form = AddRouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Маршрут успешно сохранен')
            return redirect('home')
        return render(request, 'routes/create.html', {'form': form})
    else:
        messages.error(request, "Невозможно сохранить маршрут")
        return redirect('home')


class RouteDeleteView(LoginRequiredMixin, DeleteView):
    model = Route
    template_name = 'routes/delete.html'
    success_url = reverse_lazy('list_routes')
