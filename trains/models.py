from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from cities.models import City  # Импорт моделей


class Train(models.Model):
    """ Модель поездов """
    name = models.CharField(max_length=50, unique=True, verbose_name='Название поезда')
    travel_time = models.PositiveSmallIntegerField(verbose_name='Время в пути')  # Время в пути
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='from_city_set',
                                  verbose_name='Откуда')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='to_city_set',
                                verbose_name='Куда')

    def __str__(self):
        return f'Поезд {self.name}'

    class Meta:
        verbose_name = 'Поезд'
        verbose_name_plural = 'Поезда'
        ordering = ['travel_time']

    def clean(self):
        if self.from_city == self.to_city:
            raise ValidationError('Город Прибытия = Городу Отправления')
        queryset = Train.objects.filter(
            from_city=self.from_city,
            to_city=self.to_city,
            travel_time=self.travel_time
        ).exclude(pk=self.pk)  # Исключит записи с определенными параметрами
        # Train == self.__class__
        if queryset.exists():
            raise ValidationError('Необходимо изменить время в пути')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('trains:detail', args=(self.id,))
