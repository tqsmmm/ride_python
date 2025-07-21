import json
from weather import get_weather
from core import is_good_to_ride, get_weather_summary, get_commute_suggestion

def main():
    # 加载配置
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    home_city = config['home_city']
    work_city = config['work_city']
    api_key = config['api_key']
    preferences = config['preferences']
    
    print(f"🏠 家庭城市: {home_city}")
    print(f"🏢 工作城市: {work_city}")
    
    # 判断通勤类型
    is_same_city = home_city == work_city
    commute_type = "同城通勤" if is_same_city else "跨城通勤"
    print(f"🚴 通勤类型: {commute_type}")
    
    # 获取天气信息
    print(f"\n📡 正在获取 {home_city} 的天气信息...")
    weather_data = get_weather(home_city, api_key)
    
    if weather_data:
        print(f"✅ 天气数据获取成功")
        
        # 显示天气摘要
        weather_summary = get_weather_summary(weather_data)
        print(f"\n🌤️ 天气概况:")
        print(weather_summary)
        
        # 判断是否适合骑行
        suitable, reasons = is_good_to_ride(weather_data, preferences)
        
        if suitable:
            print(f"\n✅ 今天适合骑行!")
        else:
            print(f"\n❌ 今天不太适合骑行")
            print(f"原因: {', '.join(reasons)}")
        
        # 获取通勤建议
        suggestion = get_commute_suggestion(weather_data, None, preferences, is_same_city, home_city, work_city)
        print(f"\n💡 通勤建议:")
        print(suggestion)
        
    else:
        print("❌ 无法获取天气数据，请检查网络连接和API密钥")

if __name__ == "__main__":
    main()