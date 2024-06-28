import math
from acftdata.models import An24rv_F15_Atm, An24rv_F05_Atm


def interpolate_pr_alt(pr_alt, temperature_field_name, model_class):
    pr_alt_lower = math.floor(pr_alt / 100) * 100
    pr_alt_upper = math.ceil(pr_alt / 100) * 100

    filter_kwargs_lower = {'pr_alt__exact': pr_alt_lower}
    filter_kwargs_upper = {'pr_alt__exact': pr_alt_upper}

    mtow_data_lower = model_class.objects.filter(**filter_kwargs_lower).first()
    mtow_data_upper = model_class.objects.filter(**filter_kwargs_upper).first()

    mtow_lower = getattr(mtow_data_lower, temperature_field_name, None)
    mtow_upper = getattr(mtow_data_upper, temperature_field_name, None)

    if mtow_lower is not None and mtow_upper is not None:
        alpha = (pr_alt - pr_alt_lower) / (pr_alt_upper - pr_alt_lower)
        mtow = mtow_lower + alpha * (mtow_upper - mtow_lower)
        return round(mtow) if mtow is not None else None
    else:
        return None


def interpolate_temperature(pr_alt, temperature_value, model_class):
    temperature_lower = math.floor(temperature_value / 5) * 5
    temperature_upper = math.ceil(temperature_value / 5) * 5
    temperature_field_mapping = {
        i: f't{i:02d}' for i in range(0, 50, 5)
    }

    temperature_field_name_lower = temperature_field_mapping.get(temperature_lower)
    temperature_field_name_upper = temperature_field_mapping.get(temperature_upper)

    if not temperature_field_name_lower or not temperature_field_name_upper:
        return None

    filter_kwargs = {'pr_alt__exact': pr_alt}
    mtow_data = model_class.objects.filter(**filter_kwargs).first()

    mtow_lower = getattr(mtow_data, temperature_field_name_lower, None)
    mtow_upper = getattr(mtow_data, temperature_field_name_upper, None)

    if mtow_lower is not None and mtow_upper is not None:
        alpha = (temperature_value - temperature_lower) / (temperature_upper - temperature_lower)
        mtow = mtow_lower + alpha * (mtow_upper - mtow_lower)
        return round(mtow) if mtow is not None else None
    else:
        return None


def interpolate_pr_alt_and_temperature(pr_alt, temperature_value, model_class):
    temperature_lower = math.floor(temperature_value / 5) * 5
    temperature_upper = math.ceil(temperature_value / 5) * 5
    # Расчет MTOW для двух комбинаций
    mtow_1 = interpolate_pr_alt(pr_alt, f't{temperature_lower:02d}', model_class)
    mtow_2 = interpolate_pr_alt(pr_alt, f't{temperature_upper:02d}', model_class)
    delta_temperature = temperature_value - temperature_lower
    mtow = mtow_1 - (((mtow_1 - mtow_2) / 5) * delta_temperature)
    return round(mtow) if mtow is not None else None


def calculate_mtow(temperature_value, pr_alt, flaps_position):
    flaps_position = int(flaps_position)
    try:
        temperature_value = int(temperature_value)
    except ValueError:
        temperature_value = 15  # устанавливаем значение по умолчанию
    # Установить значение в 0, если оно отрицательно
    if temperature_value < 0:
        temperature_value = 0

    temperature_field_mapping = {
        i: f't{i:02d}' for i in range(0, 50, 5)
    }

    temperature_field_name = temperature_field_mapping.get(temperature_value)

    # Determine the model based on flaps_position
    if flaps_position == 15:
        model_class = An24rv_F15_Atm
    elif flaps_position == 5:
        model_class = An24rv_F05_Atm
    else:
        return None

    if pr_alt % 100 == 0 and temperature_value % 5 == 0:
        filter_kwargs = {'pr_alt__exact': pr_alt}
        mtow_data = model_class.objects.filter(**filter_kwargs).first()
        mtow = getattr(mtow_data, temperature_field_name, None)
        return round(mtow) if mtow is not None else None

    elif pr_alt % 100 != 0 and temperature_value % 5 == 0:
        mtow = interpolate_pr_alt(pr_alt, temperature_field_name, model_class)
        return mtow if mtow is not None else None

    elif pr_alt % 100 == 0 and temperature_value % 5 != 0:
        mtow = interpolate_temperature(pr_alt, temperature_value, model_class)
        return mtow if mtow is not None else None

    else:
        # pr_alt % 100 != 0 and temperature_value % 5 != 0:
        mtow = interpolate_pr_alt_and_temperature(pr_alt, temperature_value, model_class)
        return mtow if mtow is not None else None

