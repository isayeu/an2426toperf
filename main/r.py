import math
from scipy.interpolate import interp1d
from acftdata.models import An24rv_F15_asda
from acftdata.models import An24rv_F15_tora


# Рассчет РДПВ скорректированной


def interpolate_slope_asda(asda, rw_slope):
    asda_lower = math.floor(asda / 100) * 100
    asda_upper = math.ceil(asda / 100) * 100

    # Расчет asda для двух комбинаций
    asda_1 = interpolate_slope(asda_lower, rw_slope)
    asda_2 = interpolate_slope(asda_upper, rw_slope)
    factor = (asda - asda_lower) / 100
    asda = asda_1 + ((asda_2 - asda_1) * factor)
    return asda if asda is not None else None


def interpolate_slope(asda, rw_slope):
    slope_field_name = None
    if rw_slope < 0:
        slope_field_name = 'slope_m2'
    elif rw_slope > 0:
        slope_field_name = 'slope_2'

    filter_kwargs = {'asda__exact': asda}
    asda_data = An24rv_F15_asda.objects.filter(**filter_kwargs).first()
    asda_sloped_max = getattr(asda_data, slope_field_name, None)
    interpolation_factor = abs(rw_slope) / 2
    asda = asda - (asda - asda_sloped_max) * interpolation_factor
    return asda if asda is not None else None


def interpolate_asda(asda, rw_slope):
    slope_field_name = None
    if rw_slope == -2:
        slope_field_name = 'slope_m2'
    elif rw_slope == 2:
        slope_field_name = 'slope_2'
    asda_lower = math.floor(asda / 100) * 100
    asda_upper = math.ceil(asda / 100) * 100

    filter_kwargs_lower = {'asda__exact': asda_lower}
    filter_kwargs_upper = {'asda__exact': asda_upper}

    asda_data_lower = An24rv_F15_asda.objects.filter(**filter_kwargs_lower).first()
    asda_data_upper = An24rv_F15_asda.objects.filter(**filter_kwargs_upper).first()

    asda_sloped_lower = getattr(asda_data_lower, slope_field_name, None)
    asda_sloped_upper = getattr(asda_data_upper, slope_field_name, None)

    if asda_sloped_lower is not None and asda_sloped_upper is not None:
        alpha = (asda - asda_lower) / (asda_upper - asda_lower)
        asda = asda_sloped_lower + alpha * (asda_sloped_upper - asda_sloped_lower)
        return asda if asda is not None else None
    else:
        return None


def asda_sloped(rw_slope, asda):
    slope_field_name = None
    if asda % 100 == 0 and rw_slope in [-2, 2]:
        if rw_slope == -2:
            slope_field_name = 'slope_m2'
        elif rw_slope == 2:
            slope_field_name = 'slope_2'
        filter_kwargs = {'asda__exact': asda}
        asda_data = An24rv_F15_asda.objects.filter(**filter_kwargs).first()
        asda = getattr(asda_data, slope_field_name, None)
        return asda if asda is not None else None

    elif asda % 100 != 0 and rw_slope in [-2, 2]:
        asda = interpolate_asda(asda, rw_slope)
        return asda if asda is not None else None

    elif asda % 100 == 0 and rw_slope not in [-2, 2]:
        asda = interpolate_slope(asda, rw_slope)
        return asda if asda is not None else None

    elif asda % 100 != 0 and rw_slope not in [-2, 2]:
        asda = interpolate_slope_asda(asda, rw_slope)
        return asda if asda is not None else None


def interpolate_asda_wind(asda, headwind):
    wind_mapping = {
        20: 'wind_h20',
        15: 'wind_h15',
        10: 'wind_h10',
        5: 'wind_h05',
        -5: 'wind_t05',
        -10: 'wind_t05'
    }
    wind_field_name = wind_mapping.get(headwind)
    asda_lower = math.floor(asda / 100) * 100
    asda_upper = math.ceil(asda / 100) * 100

    filter_kwargs_lower = {'asda__exact': asda_lower}
    filter_kwargs_upper = {'asda__exact': asda_upper}

    asda_data_lower = An24rv_F15_asda.objects.filter(**filter_kwargs_lower).first()
    asda_data_upper = An24rv_F15_asda.objects.filter(**filter_kwargs_upper).first()
    asda_wind_lower = getattr(asda_data_lower, wind_field_name, None)
    asda_wind_upper = getattr(asda_data_upper, wind_field_name, None)
    if asda_wind_lower is not None and asda_wind_upper is not None:
        alpha = (asda - asda_lower) / (asda_upper - asda_lower)
        asda = asda_wind_lower + alpha * (asda_wind_upper - asda_wind_lower)
        return asda if asda is not None else None
    else:
        return None


def interpolate_wind(asda, headwind):
    wind_mapping = {
        20: 'wind_h20',
        15: 'wind_h15',
        10: 'wind_h10',
        5: 'wind_h05',
        0: 'wind_00',
        -5: 'wind_t05',
        -10: 'wind_t10'
    }

    wind_values = [20, 15, 10, 5, 0, -5, -10]
    asda_values = []

    for wind_value in wind_values:
        wind_field_name = wind_mapping.get(wind_value)
        filter_kwargs = {'asda__exact': asda}
        asda_data = An24rv_F15_asda.objects.filter(**filter_kwargs).first()
        asda_value = getattr(asda_data, wind_field_name, None)
        asda_values.append(asda_value)

    f = interp1d(wind_values, asda_values, kind='cubic')
    asda = f(headwind)
    return asda


def interpolate_asda_and_wind(asda, headwind):
    asda_lower = math.floor(asda / 100) * 100
    asda_upper = math.ceil(asda / 100) * 100
    asda_1 = interpolate_wind(asda_lower, headwind)
    asda_2 = interpolate_wind(asda_upper, headwind)
    factor = (asda - asda_lower) / 100
    asda = asda_1 + ((asda_2 - asda_1) * factor)
    return asda


def asda_wind(headwind, asda):
    wind_mapping = {
        20: 'wind_h20',
        15: 'wind_h15',
        10: 'wind_h10',
        5: 'wind_h05',
        -5: 'wind_t05',
        -10: 'wind_t05'
    }
    if asda % 100 == 0 and headwind % 5 == 0:
        wind_field_name = wind_mapping.get(headwind)
        filter_kwargs = {'asda__exact': asda}
        asda_data = An24rv_F15_asda.objects.filter(**filter_kwargs).first()
        asda = getattr(asda_data, wind_field_name, None)
    elif asda % 100 != 0 and headwind % 5 == 0:
        asda = interpolate_asda_wind(asda, headwind)
    elif asda % 100 == 0 and headwind % 5 != 0:
        asda = interpolate_wind(asda, headwind)
    elif asda % 100 != 0 and headwind % 5 != 0:
        asda = interpolate_asda_and_wind(asda, headwind)
    return asda if asda is not None else None


def calculate_asda(asda_value, rw_slope_value, headwind_velocity_value):
    asda = int(asda_value)
    rw_slope = float(rw_slope_value.replace(',', '.'))  # Заменяем запятую на точку и преобразуем в float
    headwind = float(headwind_velocity_value)

    if rw_slope == 0 and headwind == 0:
        asda = asda
    elif rw_slope != 0 and headwind == 0:
        asda = asda_sloped(rw_slope, asda)
    elif rw_slope == 0 and headwind != 0:
        asda = asda_wind(headwind, asda)
    elif rw_slope != 0 and headwind != 0:
        asda = asda_sloped(rw_slope, asda)
        asda = asda_wind(headwind, asda)
    return asda

# Рассчет РДР скорректированной


def tora_interpolate_slope(rw_slope, tora_corrected):
    slope_mapping = {
        -2: 'slope_m2',
        -1: 'slope_m1',
        0: 'slope_0',
        1: 'slope_p1',
        2: 'slope_p2',
    }
    slope_values = [-2, -1, 0, 1, 2]
    tora_corrected_values = []
    for slope_value in slope_values:
        slope_field_name = slope_mapping.get(slope_value)
        filter_kwargs = {'tora__exact': tora_corrected}
        tora_data = An24rv_F15_tora.objects.filter(**filter_kwargs).first()
        tora_value = getattr(tora_data, slope_field_name, None)
        tora_corrected_values.append(tora_value)
    f = interp1d(slope_values, tora_corrected_values, kind='cubic')
    tora_corrected = f(rw_slope)
    return tora_corrected


def tora_interpolate_tora(rw_slope, tora_corrected):
    tora = tora_corrected
    tora_lower = math.floor(tora / 100) * 100
    tora_upper = math.ceil(tora / 100) * 100
    tora_1 = tora_interpolate_slope(rw_slope, tora_lower)
    tora_2 = tora_interpolate_slope(rw_slope, tora_upper)
    factor = (tora - tora_lower) / 100
    tora_corrected = tora_1 + ((tora_2 - tora_1) * factor)
    return tora_corrected


def tora_slope_calculate(rw_slope, tora_corrected):
    slope_mapping = {
        -2: 'slope_m2',
        -1: 'slope_m1',
        0: 'slope_0',
        1: 'slope_p1',
        2: 'slope_p2',
    }

    if tora_corrected % 100 == 0 and rw_slope % 1 == 0:
        slope_field_name = slope_mapping.get(rw_slope)
        filter_kwargs = {'tora__exact': tora_corrected}
        tora_data = An24rv_F15_tora.objects.filter(**filter_kwargs).first()
        tora_corrected = getattr(tora_data, slope_field_name, None)
    elif tora_corrected % 100 == 0 and rw_slope % 1 != 0:
        tora_corrected = tora_interpolate_slope(rw_slope, tora_corrected)
    elif tora_corrected % 100 != 0:
        tora_corrected = tora_interpolate_tora(rw_slope, tora_corrected)
    return tora_corrected


def tora_interpolate_wind(tora, headwind):
    wind_mapping = {
        20: 'wind_h20',
        15: 'wind_h15',
        10: 'wind_h10',
        5: 'wind_h05',
        0: 'wind_00',
        -5: 'wind_t05',
        -10: 'wind_t05'
    }
    wind_values = [20, 15, 10, 5, 0, -5, -10]
    tora_values = []
    for wind_value in wind_values:
        wind_field_name = wind_mapping.get(wind_value)
        filter_kwargs = {'tora__exact': tora}
        tora_data = An24rv_F15_tora.objects.filter(**filter_kwargs).first()
        tora_value = getattr(tora_data, wind_field_name, None)
        tora_values.append(tora_value)

    f = interp1d(wind_values, tora_values, kind='cubic')
    tora = f(headwind)
    return tora


def tora_interpolate_tora_by_wind(tora, headwind):
    tora_lower = math.floor(tora / 100) * 100
    tora_upper = math.ceil(tora / 100) * 100
    tora_1 = tora_interpolate_wind(tora_lower, headwind)
    tora_2 = tora_interpolate_wind(tora_upper, headwind)
    factor = (tora - tora_lower) / 100
    tora = tora_1 + ((tora_2 - tora_1) * factor)
    return tora


def tora_wind_calculate(tora_corrected, headwind):
    tora = tora_corrected
    wind_mapping = {
        20: 'wind_h20',
        15: 'wind_h15',
        10: 'wind_h10',
        5: 'wind_h05',
        -5: 'wind_t05',
        -10: 'wind_t05'
    }
    if tora % 100 == 0 and headwind % 5 == 0:
        wind_field_name = wind_mapping.get(headwind)
        filter_kwargs = {'tora__exact': tora}
        tora_data = An24rv_F15_tora.objects.filter(**filter_kwargs).first()
        tora = getattr(tora_data, wind_field_name, None)
        tora_corrected = tora
    elif tora % 100 == 0 and headwind % 5 != 0:
        tora_corrected = tora_interpolate_wind(tora, headwind)
    elif tora % 100 != 0:
        tora_corrected = tora_interpolate_tora_by_wind(tora, headwind)
    return tora_corrected


def calculate_tora(tora_value, rw_slope_value, headwind_velocity_value):
    tora_corrected = tora_value
    rw_slope = float(rw_slope_value.replace(',', '.'))  # Заменяем запятую на точку и преобразуем в float
    headwind = float(headwind_velocity_value)
    if rw_slope == 0 and headwind == 0:
        tora_corrected = tora_corrected
    elif rw_slope != 0 and headwind == 0:
        tora_corrected = tora_slope_calculate(rw_slope, tora_corrected)
    elif rw_slope == 0 and headwind != 0:
        tora_corrected = tora_wind_calculate(tora_corrected, headwind)
    elif rw_slope != 0 and headwind != 0:
        tora_corrected = tora_slope_calculate(rw_slope, tora_corrected)
        tora_corrected = tora_wind_calculate(tora_corrected, headwind)
    return tora_corrected
