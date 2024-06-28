from django.shortcuts import render
from .forms import AirportsForm, WeatherForm, RunwayForm, AircraftForm
from .models import Airports
from .praltitude import pressure_altitude_calculated
from .wind import calculate_wind
from .mtow import calculate_mtow
from .r import calculate_asda
from .r import calculate_tora

flaps_position = None


def index_page(request):
    global flaps_position
    # Инициализация форм
    qnh_form = WeatherForm(request.POST or None)
    icao_form = AirportsForm(request.POST or None)
    temperature_form = WeatherForm(request.POST or None)
    wind_direction_form = WeatherForm(request.POST or None)
    wind_velocity_form = WeatherForm(request.POST or None)
    flaps_settings_form = AircraftForm(request.POST)
    tora_form = RunwayForm(request.POST or None)
    asda_form = RunwayForm(request.POST or None)
    rw_slope_form = RunwayForm(request.POST or None)

    # Инициализация переменных
    qnh_value = ''
    airport_data = None
    temperature_value = ''
    wind_direction_value = ''
    wind_velocity_value = ''
    to_heading_value = ''
    flaps_position = 15
    tora_value = ''
    asda_value = ''
    rw_slope_value = ''

    # Если запрос не POST, установите tora_value в пустую строку
    if request.method != 'POST':
        rw_slope_value = ''
    # Если запрос не POST, установите tora_value в пустую строку
    if request.method != 'POST':
        tora_value = ''
    # Если запрос не POST, установите asda_value в пустую строку
    if request.method != 'POST':
        asda_value = ''
    # Если запрос не POST, установите to_heading_value в пустую строку
    if request.method != 'POST':
        to_heading_value = ''
    # Если запрос не POST, установите qnh_value в пустую строку
    if request.method != 'POST':
        qnh_value = ''
    # Если запрос не POST, установите temperature_value в пустую строку
    if request.method != 'POST':
        temperature_value = ''
    # Если запрос не POST, установите wind_direction_value в пустую строку
    if request.method != 'POST':
        wind_direction_value = ''
    # Если запрос не POST, установите wind_velocity_value в пустую строку
    if request.method != 'POST':
        wind_velocity_value = ''

    if request.method == 'POST':
        to_heading_form = RunwayForm(request.POST)
        if to_heading_form.is_valid():
            to_heading_value = to_heading_form.cleaned_data.get('to_heading')

    if request.method == 'POST':
        if rw_slope_form.is_valid():
            rw_slope_value = rw_slope_form.cleaned_data.get('rw_slope', '0')
            if not rw_slope_value:
                rw_slope_value = '0'

    if request.method == 'POST':
        if tora_form.is_valid():
            tora_value = tora_form.cleaned_data.get('tora', '0')
            if not tora_value:
                tora_value = '0'

    if request.method == 'POST':
        if asda_form.is_valid():
            asda_value = asda_form.cleaned_data.get('asda', '0')
            if not asda_value:
                asda_value = '0'

    if request.method == 'POST':
        if qnh_form.is_valid():
            qnh_value = qnh_form.cleaned_data.get('qnh', '1013')
            if not qnh_value:
                qnh_value = '1013'

    if request.method == 'POST':
        if temperature_form.is_valid():
            temperature_value = temperature_form.cleaned_data.get('temperature', '15')
            if not temperature_value:
                temperature_value = '15'

    if request.method == 'POST':
        if wind_direction_form.is_valid():
            wind_direction_value = temperature_form.cleaned_data.get('wind_direction', '0')
            if not wind_direction_value:
                wind_direction_value = '0'

    if request.method == 'POST':
        if wind_velocity_form.is_valid():
            wind_velocity_value = temperature_form.cleaned_data.get('wind_velocity', '0')
            if not wind_velocity_value:
                wind_velocity_value = '0'

    if request.method == 'POST':
        if flaps_settings_form.is_valid():
            flaps_position = flaps_settings_form.cleaned_data.get('flaps_position')

    if icao_form.is_valid():
        icao_value = icao_form.cleaned_data['ICAO']
        airport_data = Airports.objects.filter(ICAO__iexact=icao_value).first()

    # барометрическая высота
    pr_alt = 0
    if airport_data:
        airport_data.pressure_altitude = int(pressure_altitude_calculated(airport_data.alevation, int(qnh_value)))
        pr_alt = airport_data.pressure_altitude

    # Встречная состовляющая ветра
    headwind = calculate_wind(to_heading_value, wind_direction_value, wind_velocity_value)
    if headwind is not None:
        headwind_velocity_value = round(headwind, 1)
    else:
        # Обработка случая, когда calculate_wind возвращает None
        headwind_velocity_value = None  # Или установите значение по умолчанию или что-то еще

    asda_corrected = asda_value
    if asda_value != '':
        if int(asda_value) > 3000:
            asda_value = 3000
        asda_corrected = calculate_asda(asda_value, rw_slope_value, headwind_velocity_value)
        asda_corrected = round(int(asda_corrected))

    tora_corrected = tora_value
    if tora_value != '':
        if int(tora_value) > 3500:
            tora_value = 3500
        tora_corrected = calculate_tora(tora_value, rw_slope_value, headwind_velocity_value)
        tora_corrected = round(float(tora_corrected))

    # MTOW
    mtow_value = calculate_mtow(temperature_value, pr_alt, flaps_position)

    # Вернуть обновленный контекст в шаблон
    return render(request, 'index.html', {
        'to_heading_value': to_heading_value,
        'qnh_value': qnh_value,
        'rw_slope_value': rw_slope_value,
        'tora_value': tora_value,
        'tora_corrected': tora_corrected,
        'asda_value': asda_value,
        'asda_corrected': asda_corrected,
        'temperature_value': temperature_value,
        'wind_direction_value': wind_direction_value,
        'wind_velocity_value': wind_velocity_value,
        'headwind_velocity_value': headwind_velocity_value,
        'icao_form': icao_form,
        'airport_data': airport_data,
        'flaps_settings_form': flaps_settings_form,
        'flaps_position': flaps_position,
        'mtow_value': mtow_value
    })


def about_page(request):
    return render(request, 'about.html')
