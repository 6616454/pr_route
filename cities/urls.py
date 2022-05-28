from django.urls import path
import cities.views as views

app_name = 'cities'

urlpatterns = [
    path('', views.home, name='home'),
    path('city/<int:pk>/', views.CityDetailView.as_view(), name='detail'),
    path('create/', views.CityCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.CityUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.CityDeleteView.as_view(), name='delete')
]
