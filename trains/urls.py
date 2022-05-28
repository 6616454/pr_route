from django.urls import path
import trains.views as views

app_name = 'trains'

urlpatterns = [
    path('', views.home, name='home'),
    path('train/<int:pk>/', views.TrainDetailView.as_view(), name='detail'),
    path('create/', views.TrainCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.TrainUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.TrainDeleteView.as_view(), name='delete')
]
