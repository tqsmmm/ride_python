import json
from geocoding import get_coordinates, get_city_from_address
from weather import get_weather
from core import is_good_to_ride, get_commute_suggestion

def main():
    """主函数"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("错误：找不到 config.json 文件。请确保该文件存在并已正确配置。")
        return

    home_address = config['home_address']
    work_address = config['work_address']
    api_key = config['api_key']
    preferences = config['preferences']

    print(f"正在分析通勤路线...")
    print(f"家庭地址: {home_address}")
    print(f"工作地址: {work_address}")

    # 获取家庭地址坐标
    print(f"\n正在获取'{home_address}'的坐标...")
    home_lat, home_lon = get_coordinates(home_address)
    if not home_lat or not home_lon:
        print("无法获取家庭地址的坐标，请检查地址是否正确。")
        return

    # 获取工作地址坐标
    print(f"正在获取'{work_address}'的坐标...")
    work_lat, work_lon = get_coordinates(work_address)
    if not work_lat or not work_lon:
        print("无法获取工作地址的坐标，请检查地址是否正确。")
        return

    # 判断是否为同城通勤
    home_city = get_city_from_address(home_address)
    work_city = get_city_from_address(work_address)
    is_same_city = home_city == work_city

    print(f"\n通勤类型: {'同城通勤' if is_same_city else '跨城通勤'}")
    if not is_same_city:
        print(f"家庭城市: {home_city}")
        print(f"工作城市: {work_city}")

    # 获取天气信息
    print("\n正在获取天气信息...")
    home_weather = get_weather(home_lat, home_lon, api_key)
    if not home_weather:
        print("无法获取家庭地址天气信息，请检查你的 API 密钥是否有效。")
        return

    work_weather = None
    if not is_same_city:
        work_weather = get_weather(work_lat, work_lon, api_key)
        if not work_weather:
            print("无法获取工作地址天气信息，将仅基于家庭地址天气给出建议。")

    # 生成骑行建议
    suggestion = get_commute_suggestion(
        home_weather, work_weather, preferences, 
        is_same_city, home_city, work_city
    )

    print("\n" + "="*50)
    print("🚴‍♂️ 智能通勤骑行建议")
    print("="*50)
    print(suggestion)
    print("="*50)

if __name__ == "__main__":
    main()