"""travel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

from routes.views import home, find_routes, add_routes, save_routes, route_list, RouteDetailView, RouteDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cities/', include('cities.urls', namespace='cities')),
    path('trains/', include('trains.urls', namespace='trains')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', home, name='home'),
    path('find_routes/', find_routes, name='find_routes'),
    path('add_routes/', add_routes, name='add_routes'),
    path('save_routes/', save_routes, name='save_routes'),
    path('list_routes/', route_list, name='list_routes'),
    path('detail_routes/<int:pk>/', RouteDetailView.as_view(), name='detail_routes'),
    path('delete_routes/<int:pk>/', RouteDeleteView.as_view(), name='delete_routes')
]
