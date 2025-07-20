
import json
from geocoding import get_coordinates
from weather import get_weather
from core import is_good_to_ride

def main():
    """主函数"""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("错误：找不到 config.json 文件。请确保该文件存在并已正确配置。")
        return

    home_address = config['home_address']
    work_address = config['work_address']
    api_key = config['api_key']
    preferences = config['preferences']

    print(f"正在获取‘{home_address}’的坐标...")
    home_lat, home_lon = get_coordinates(home_address)

    if not home_lat or not home_lon:
        print("无法获取家庭地址的坐标，请检查地址是否正确。")
        return

    print("正在获取天气信息...")
    weather_data = get_weather(home_lat, home_lon, api_key)

    if not weather_data:
        print("无法获取天气信息，请检查你的 API 密钥是否有效。")
        return

    ride, message = is_good_to_ride(weather_data, preferences)

    print("\n--- 通勤骑行建议 ---")
    print(message)
    print("--------------------\n")

if __name__ == "__main__":
    main()
