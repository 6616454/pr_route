from django.db import models
from django.urls import reverse

from cities.models import City
from trains.models import Train


class Route(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название маршрута')
    all_time = models.PositiveSmallIntegerField(verbose_name='Общее время пути')
    from_city = models.ForeignKey(City, on_delete=models.CASCADE,
                                  related_name='route_from_city_set',
                                  verbose_name='Из какого города')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE,
                                related_name='route_to_city_set',
                                verbose_name='В какой город')
    trains = models.ManyToManyField(Train, verbose_name='Список поездов')

    def __str__(self):
        return f"Маршрут {self.name} из города {self.from_city}"

    def get_absolute_url(self):
        return reverse('detail_routes', args=(self.id,))

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        ordering = ['all_time']
