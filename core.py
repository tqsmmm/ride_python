
def parse_address(address):
    """解析地址，提取城市和区信息
    
    Args:
        address: 地址字符串，如"鞍山市铁东区"、"北京市朝阳区"
    
    Returns:
        tuple: (城市, 区) 如("鞍山市", "铁东区")
    """
    # 处理常见的地址格式
    if '市' in address:
        parts = address.split('市')
        if len(parts) >= 2:
            city = parts[0] + '市'
            district = parts[1] if parts[1] else None
            return city, district
        else:
            # 只有城市，没有区
            return address, None
    else:
        # 没有"市"字符，可能是特殊格式
        return address, None

def get_commute_type(home_address, work_address):
    """判断通勤类型
    
    Args:
        home_address: 家庭地址
        work_address: 工作地址
    
    Returns:
        tuple: (通勤类型, 是否同城, 是否同区)
    """
    home_city, home_district = parse_address(home_address)
    work_city, work_district = parse_address(work_address)
    
    # 判断是否同城
    is_same_city = home_city == work_city
    
    # 判断是否同区（只有在同城的情况下才有意义）
    is_same_district = is_same_city and home_district == work_district and home_district is not None
    
    if is_same_district:
        commute_type = "同区通勤"
    elif is_same_city:
        commute_type = "同城跨区通勤"
    else:
        commute_type = "跨城通勤"
    
    return commute_type, is_same_city, is_same_district

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

def get_commute_suggestion(home_weather, work_weather, preferences, commute_type, is_same_city, is_same_district, home_address, work_address):
    """根据家庭和工作地址天气情况给出通勤骑行建议"""
    
    # 分析家庭地址天气
    home_suitable, home_message = is_good_to_ride(home_weather, preferences)
    home_summary = get_weather_summary(home_weather)
    
    suggestion = f"📍 家庭地址 ({home_address}):\n{home_summary}\n"
    
    if commute_type == "同区通勤":
        # 同区通勤 - 距离最短，最适合骑行
        suggestion += f"\n🏠➡️🏢 同区通勤建议:\n"
        if home_suitable:
            suggestion += f"✅ {home_message}\n"
            suggestion += f"💡 建议: 同区通勤距离较短，天气条件良好，非常适合骑行！\n"
            suggestion += f"   • 预计骑行时间: 10-20分钟\n"
            suggestion += f"   • 优势: 环保健康，避免交通拥堵，节省交通费\n"
            suggestion += f"   • 提醒: 注意交通安全，佩戴头盔"
        else:
            suggestion += f"❌ {home_message}\n"
            suggestion += f"💡 建议: 虽然距离较短，但天气条件不佳，建议选择其他方式\n"
            suggestion += f"   • 推荐: 公交、地铁或打车\n"
            suggestion += f"   • 备选: 如果有室内停车场，可考虑电动车"
            
    elif commute_type == "同城跨区通勤":
        # 同城跨区通勤 - 中等距离，需要考虑体力和时间，现在也要考虑工作地址天气
        work_summary = get_weather_summary(work_weather) if work_weather else "无法获取工作地址天气"
        work_suitable = False
        work_message = "无法获取工作地址天气数据"
        
        if work_weather:
            work_suitable, work_message = is_good_to_ride(work_weather, preferences)
            suggestion += f"\n📍 工作地址 ({work_address}):\n{work_summary}\n"
        
        suggestion += f"\n🏠➡️🏢 同城跨区通勤建议:\n"
        
        if work_weather:
            # 有工作地址天气数据，综合考虑两地天气
            if home_suitable and work_suitable:
                suggestion += f"✅ 两地天气都适合骑行\n"
                suggestion += f"💡 建议: 同城跨区通勤，两地天气条件都良好，推荐骑行！\n"
                suggestion += f"   • 预计骑行时间: 20-40分钟\n"
                suggestion += f"   • 适合人群: 有一定体力基础，时间相对充裕\n"
                suggestion += f"   • 准备事项: 带好水壶，规划好路线，避开拥堵路段\n"
                suggestion += f"   • 路线建议: 选择自行车道或车流量较少的道路\n"
                suggestion += f"   • 备选方案: 公交+共享单车组合"
            elif home_suitable and not work_suitable:
                suggestion += f"⚠️  家庭地址适合骑行，但工作地址天气不佳\n"
                suggestion += f"💡 建议: 出发时天气良好，但目的地天气不适合，需要谨慎考虑\n"
                suggestion += f"   • 风险评估: 到达工作地点时可能遇到恶劣天气\n"
                suggestion += f"   • 推荐方案: 地铁、公交等有遮挡的交通方式\n"
                suggestion += f"   • 备选: 如果工作地点有室内停车，可考虑骑行但准备雨具\n"
                suggestion += f"   • 工作地址天气: {work_message}"
            elif not home_suitable and work_suitable:
                suggestion += f"⚠️  工作地址适合骑行，但家庭地址天气不佳\n"
                suggestion += f"💡 建议: 出发地天气不佳，不建议骑行出发\n"
                suggestion += f"   • 推荐: 乘坐公共交通到工作地点\n"
                suggestion += f"   • 考虑: 下班时如果天气好转，可考虑骑共享单车\n"
                suggestion += f"   • 家庭地址天气: {home_message}"
            else:
                suggestion += f"❌ 两地天气都不适合骑行\n"
                suggestion += f"💡 建议: 两地天气条件都不佳，强烈建议选择其他交通方式\n"
                suggestion += f"   • 推荐: 地铁、公交等公共交通\n"
                suggestion += f"   • 家庭地址: {home_message}\n"
                suggestion += f"   • 工作地址: {work_message}"
        else:
            # 没有工作地址天气数据，只基于家庭地址天气判断
            if home_suitable:
                suggestion += f"✅ {home_message}\n"
                suggestion += f"💡 建议: 同城跨区通勤，家庭地址天气条件良好，可以考虑骑行\n"
                suggestion += f"   • 预计骑行时间: 20-40分钟\n"
                suggestion += f"   • 适合人群: 有一定体力基础，时间相对充裕\n"
                suggestion += f"   • 准备事项: 带好水壶，规划好路线，避开拥堵路段\n"
                suggestion += f"   • 注意: 无法获取工作地址天气，建议关注路途天气变化\n"
                suggestion += f"   • 备选方案: 公交+共享单车组合"
            else:
                suggestion += f"❌ {home_message}\n"
                suggestion += f"💡 建议: 跨区距离较长，天气条件不佳，不建议骑行\n"
                suggestion += f"   • 推荐: 地铁、公交等公共交通\n"
                suggestion += f"   • 考虑: 如果部分路段有地铁，可地铁+短途骑行"
            
    else:
        # 跨城通勤 - 距离最长，一般不建议骑行
        work_summary = get_weather_summary(work_weather) if work_weather else "无法获取工作地址天气"
        work_suitable = False
        work_message = "无法获取工作地址天气数据"
        
        if work_weather:
            work_suitable, work_message = is_good_to_ride(work_weather, preferences)
        
        suggestion += f"\n📍 工作地址 ({work_address}):\n{work_summary}\n"
        suggestion += f"\n🏠➡️🏢 跨城通勤建议:\n"
        
        if home_suitable and work_suitable:
            suggestion += f"✅ 两地天气都适合骑行\n"
            suggestion += f"💡 建议: 跨城通勤距离较远，即使天气良好也需谨慎考虑:\n"
            suggestion += f"   • 距离评估: 如果 < 30km 且体力充沛，可偶尔尝试\n"
            suggestion += f"   • 时间成本: 预计需要1-2小时，需要早起\n"
            suggestion += f"   • 推荐方案: 高铁/城际+共享单车的组合方式\n"
            suggestion += f"   • 周末选择: 可作为健身骑行，平时建议公共交通"
        elif home_suitable and not work_suitable:
            suggestion += f"⚠️  家庭地址适合骑行，但工作地址天气不佳\n"
            suggestion += f"💡 建议: 跨城通勤不建议骑行，特别是目的地天气不好\n"
            suggestion += f"   • 推荐: 高铁、城际铁路或长途客车\n"
            suggestion += f"   • 工作地址天气: {work_message}"
        elif not home_suitable and work_suitable:
            suggestion += f"⚠️  工作地址适合骑行，但家庭地址天气不佳\n"
            suggestion += f"💡 建议: 出发地天气不佳，不建议骑行通勤\n"
            suggestion += f"   • 推荐: 公共交通到达后，考虑当地短途骑行\n"
            suggestion += f"   • 家庭地址天气: {home_message}"
        else:
            suggestion += f"❌ 两地天气都不适合骑行\n"
            suggestion += f"💡 建议: 跨城通勤且天气不佳，强烈建议公共交通\n"
            suggestion += f"   • 家庭地址: {home_message}\n"
            suggestion += f"   • 工作地址: {work_message if work_weather else '无法获取天气数据'}\n"
            suggestion += f"   • 推荐: 高铁、城际铁路等快速交通工具"
    
    return suggestion

