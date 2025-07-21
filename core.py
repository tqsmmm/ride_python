
def is_good_to_ride(weather_data, preferences):
    """根据天气数据和偏好判断是否适合骑行"""
    if not weather_data:
        return False, "无法获取天气数据。"

    temp = weather_data['main']['temp']
    wind_speed = weather_data['wind']['speed']
    weather_condition = weather_data['weather'][0]['main']

    # 温度检查
    if temp < preferences['min_temp']:
        return False, f"太冷了！当前温度 {temp}°C 低于你设置的最低温度 {preferences['min_temp']}°C。"
    if temp > preferences['max_temp']:
        return False, f"太热了！当前温度 {temp}°C 高于你设置的最高温度 {preferences['max_temp']}°C。"
    
    # 风速检查
    if wind_speed > preferences['max_wind_speed']:
        return False, f"风太大了！当前风速 {wind_speed:.1f} m/s 超过了你设置的最大风速 {preferences['max_wind_speed']} m/s。"
    
    # 降水检查 - 和风天气的降水相关天气条件
    rain_conditions = ['雨', '阵雨', '雷阵雨', '小雨', '中雨', '大雨', '暴雨', '毛毛雨', '冻雨']
    snow_conditions = ['雪', '阵雪', '小雪', '中雪', '大雪', '暴雪', '雨夹雪']
    
    if not preferences['allow_rain']:
        if any(condition in weather_condition for condition in rain_conditions + snow_conditions):
            return False, f"当前天气为'{weather_condition}'，你设置了不允许雨雪天骑行。"

    return True, f"天气不错，适合骑行！当前温度 {temp}°C，风速 {wind_speed:.1f} m/s，天气状况：{weather_condition}"

def get_weather_summary(weather_data):
    """获取天气摘要信息"""
    if not weather_data:
        return "无天气数据"
    
    temp = weather_data['main']['temp']
    wind_speed = weather_data['wind']['speed']
    weather_condition = weather_data['weather'][0]['main']
    humidity = weather_data['main']['humidity']
    
    return f"温度: {temp}°C | 风速: {wind_speed:.1f}m/s | 天气: {weather_condition} | 湿度: {humidity}%"

def get_commute_suggestion(home_weather, work_weather, preferences, is_same_city, home_city, work_city):
    """根据家庭和工作地址天气情况给出通勤骑行建议"""
    
    # 分析家庭地址天气
    home_suitable, home_message = is_good_to_ride(home_weather, preferences)
    home_summary = get_weather_summary(home_weather)
    
    suggestion = f"📍 家庭地址 ({home_city}):\n{home_summary}\n"
    
    if is_same_city:
        # 同城通勤
        suggestion += f"\n🏠➡️🏢 同城通勤建议:\n"
        if home_suitable:
            suggestion += f"✅ {home_message}\n"
            suggestion += f"💡 建议: 天气条件良好，适合骑行通勤！记得做好防护措施。"
        else:
            suggestion += f"❌ {home_message}\n"
            suggestion += f"💡 建议: 建议选择其他交通方式，如地铁、公交或打车。"
    else:
        # 跨城通勤
        work_summary = get_weather_summary(work_weather) if work_weather else "无法获取工作地址天气"
        work_suitable = False
        work_message = "无法获取工作地址天气数据"
        
        if work_weather:
            work_suitable, work_message = is_good_to_ride(work_weather, preferences)
        
        suggestion += f"\n📍 工作地址 ({work_city}):\n{work_summary}\n"
        suggestion += f"\n🏠➡️🏢 跨城通勤建议:\n"
        
        if home_suitable and work_suitable:
            suggestion += f"✅ 两地天气都适合骑行\n"
            suggestion += f"💡 建议: 由于是跨城通勤，建议考虑以下方案:\n"
            suggestion += f"   • 如果距离较近(< 20km): 可以尝试骑行，但要准备充足的体力和时间\n"
            suggestion += f"   • 如果距离较远: 建议公共交通+短途骑行的组合方式\n"
            suggestion += f"   • 备选方案: 准备雨具和保暖衣物，以应对路途中的天气变化"
        elif home_suitable and not work_suitable:
            suggestion += f"⚠️  家庭地址适合骑行，但工作地址天气不佳\n"
            suggestion += f"💡 建议: 不建议骑行通勤，因为到达工作地点时天气条件不适合\n"
            suggestion += f"   • 推荐: 选择公共交通工具\n"
            suggestion += f"   • 工作地址天气: {work_message}"
        elif not home_suitable and work_suitable:
            suggestion += f"⚠️  工作地址适合骑行，但家庭地址天气不佳\n"
            suggestion += f"💡 建议: 不建议从家骑行出发\n"
            suggestion += f"   • 推荐: 乘坐公共交通到工作地点附近，考虑短途骑行\n"
            suggestion += f"   • 家庭地址天气: {home_message}"
        else:
            suggestion += f"❌ 两地天气都不适合骑行\n"
            suggestion += f"💡 建议: 强烈建议选择其他交通方式\n"
            suggestion += f"   • 家庭地址: {home_message}\n"
            suggestion += f"   • 工作地址: {work_message if work_weather else '无法获取天气数据'}"
    
    return suggestion

