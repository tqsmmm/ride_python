
def is_good_to_ride(weather_data, preferences):
    """根据天气数据和偏好判断是否适合骑行"""
    if not weather_data:
        return False, "无法获取天气数据。"

    temp = weather_data['main']['temp']
    wind_speed = weather_data['wind']['speed']
    weather_condition = weather_data['weather'][0]['main'].lower()

    if temp < preferences['min_temp']:
        return False, f"太冷了！当前温度 {temp}°C 低于你设置的最低温度 {preferences['min_temp']}°C。"
    if temp > preferences['max_temp']:
        return False, f"太热了！当前温度 {temp}°C 高于你设置的最高温度 {preferences['max_temp']}°C。"
    if wind_speed > preferences['max_wind_speed']:
        return False, f"风太大了！当前风速 {wind_speed} m/s 超过了你设置的最大风速 {preferences['max_wind_speed']} m/s。"
    if not preferences['allow_rain'] and 'rain' in weather_condition:
        return False, "天在下雨，你设置了不允许雨天骑行。"

    return True, "天气不错，适合骑行！"

