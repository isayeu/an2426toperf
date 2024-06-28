from math import cos, radians


def calculate_wind(to_heading, wind_direction, wind_velocity):
    # Проверяем, что значения не пустые
    if not wind_direction or not to_heading:
        # Возвращаем какое-то значение по умолчанию или обрабатываем этот случай по вашему усмотрению
        return None

    try:
        # Пробуем преобразовать значения в целые числа
        to_heading = int(to_heading)
        wind_direction = int(wind_direction)
        wind_velocity = float(wind_velocity)

        wind_angle = (wind_direction - to_heading) % 360
        if wind_angle <= 180:
            # wind_type = "Headwind" if wind_angle <= 89 else "Tailwind"
            wind_angle = 180 - wind_angle
        else:
            # wind_type = "Headwind" if wind_angle >= 271 else "Tailwind"
            wind_angle = wind_angle - 180

        wind_angle_radians = radians(wind_angle)  # Преобразуем угол в радианы

        headwind = wind_velocity * cos(wind_angle_radians) * (-1)
        # crosswind = wind_velocity * abs(sin(wind_angle_radians))

        return headwind

    except ValueError:
        # Обрабатываем случай, если значения невозможно преобразовать в числа
        return None
