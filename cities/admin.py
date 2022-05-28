from django.contrib import admin
from .models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
