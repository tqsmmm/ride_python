import json
from weather import get_weather
from core import is_good_to_ride, get_weather_summary, get_commute_suggestion, get_commute_type

def main():
    # 加载配置
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    home_city = config['home_city']
    work_city = config['work_city']
    api_key = config['api_key']
    preferences = config['preferences']
    
    print(f"🏠 家庭地址: {home_city}")
    print(f"🏢 工作地址: {work_city}")
    
    # 判断通勤类型
    commute_type, is_same_city, is_same_district = get_commute_type(home_city, work_city)
    print(f"🚴 通勤类型: {commute_type}")
    
    # 获取家庭地址天气信息
    print(f"\n📡 正在获取 {home_city} 的天气信息...")
    home_weather_data = get_weather(home_city, api_key)
    
    # 初始化工作地址天气数据
    work_weather_data = None
    
    # 判断是否需要获取工作地址天气（只要不是同区通勤就需要获取）
    if not is_same_district:
        print(f"📡 正在获取 {work_city} 的天气信息...")
        work_weather_data = get_weather(work_city, api_key)
        
        if work_weather_data:
            print(f"✅ 工作地址天气数据获取成功")
        else:
            print(f"⚠️  工作地址天气数据获取失败")
    
    if home_weather_data:
        print(f"✅ 家庭地址天气数据获取成功")
        
        # 显示家庭地址天气摘要
        home_weather_summary = get_weather_summary(home_weather_data)
        print(f"\n🌤️ 家庭地址天气概况:")
        print(home_weather_summary)
        
        # 如果有工作地址天气，也显示
        if work_weather_data:
            work_weather_summary = get_weather_summary(work_weather_data)
            print(f"\n🌤️ 工作地址天气概况:")
            print(work_weather_summary)
        
        # 基于家庭地址天气判断是否适合骑行（作为总体参考）
        suitable, reasons = is_good_to_ride(home_weather_data, preferences)
        
        if suitable:
            print(f"\n✅ 从天气角度看，今天适合骑行!")
        else:
            print(f"\n❌ 从天气角度看，今天不太适合骑行")
            print(f"原因: {reasons}")
        
        # 获取通勤建议（现在会考虑两地天气）
        suggestion = get_commute_suggestion(
            home_weather_data, 
            work_weather_data, 
            preferences, 
            commute_type, 
            is_same_city, 
            is_same_district, 
            home_city, 
            work_city
        )
        print(f"\n💡 通勤建议:")
        print(suggestion)
        
    else:
        print("❌ 无法获取家庭地址天气数据，请检查网络连接和API密钥")

if __name__ == "__main__":
    main()