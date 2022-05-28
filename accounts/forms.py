from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model()


class LoginUserForm(forms.Form):
    username = forms.CharField(
        label='username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите username'
        })
    )
    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите password'
        })
    )

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            queryset = User.objects.filter(username=username)
            if not queryset.exists():
                raise forms.ValidationError('Такого пользователя нет')
            if not check_password(password, queryset[0].password):
                raise forms.ValidationError('Неверный пароль')

            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Данный пользователь неактивен')

        return super().clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите username'
        })
    )
    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите password'
        })
    )
    password2 = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите password'
        })
    )

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError
        return data['password2']

    class Meta:
        model = User
        fields = ('username',)
