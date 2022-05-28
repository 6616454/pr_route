from django.contrib import admin
from .models import Train


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    """ Админка Поездов """
    list_display = ('id', 'name', 'travel_time', 'from_city', 'to_city')
    list_editable = ('travel_time',)
