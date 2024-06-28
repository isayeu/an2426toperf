from django import forms
from django.forms import ModelForm, TextInput
from .models import Airports


class AircraftForm(forms.Form):
    flaps_settings = [
        (15, 'Закрылки 15'),
        (5, 'Закрылки 5'),
    ]
    flaps_position = forms.ChoiceField(choices=flaps_settings, initial=15)


class WeatherForm(forms.Form):
    qnh = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'QNH'}), required=False)
    temperature = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Температура'}), required=False)
    wind_direction = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Направление ветра'}), required=False)
    wind_velocity = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Скорость ветра'}), required=False)


class RunwayForm(forms.Form):
    to_heading = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Курс взлета'}), required=True)
    tora = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'РДР'}), required=False)
    asda = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'РДПВ'}), required=False)
    rw_slope = forms.Field(widget=forms.NumberInput(attrs={'placeholder': 'Уклон ВПП'}), required=False)


class AirportsForm(ModelForm):
    class Meta:
        model = Airports
        fields = ['ICAO']
        widgets = {
            "ICAO": TextInput(attrs={
                'placeholder': 'ICAO Index',
                'style': 'text-transform: uppercase;',
                'oninput': 'this.value = this.value.replace(/[^A-Za-z]/g, "")',
                'required': 'required',
            }),
        }
