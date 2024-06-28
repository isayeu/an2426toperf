def pressure_altitude_calculated(feet, qnh_value):
    alevation_in_meters = feet * 0.3048
    delta_hpa = 1013 - qnh_value
    delta_in_meters = delta_hpa * 8
    return alevation_in_meters + delta_in_meters

