from django import forms
from cities.models import City
from routes.models import Route
from trains.models import Train


class RouteForm(forms.Form):
    """ Форма поиска маршрута """
    # name = forms.CharField(label='Номер поезда', widget=forms.TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Введите номер поезда'
    # }))
    from_city = forms.ModelChoiceField(
        label='Откуда', queryset=City.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control js-example-basic-single'
            }
        )
    )
    to_city = forms.ModelChoiceField(
        label='Куда', queryset=City.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control js-example-basic-single'
            }
        )
    )
    cities = forms.ModelMultipleChoiceField(
        label='Через какие города',
        queryset=City.objects.all(),
        required=False,  # Необязательное поле
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control js-example-basic-multiple'
            }
        )
    )
    all_time = forms.IntegerField(label='Время пути', widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите время пути'
    }))


class AddRouteForm(forms.ModelForm):
    """ Форма добавления маршрута """
    name = forms.CharField(
        label='Название маршрута',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название маршрута'
        })
    )
    from_city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=forms.HiddenInput()
    )

    to_city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=forms.HiddenInput()
    )

    trains = forms.ModelMultipleChoiceField(
        queryset=Train.objects.all(),
        required=False,  # Необязательное поле
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control d-none'
            }
        )
    )
    all_time = forms.IntegerField(
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Route
        fields = '__all__'
