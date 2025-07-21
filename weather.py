
import requests

def get_city_id(city_name, api_key):
    """通过城市名称获取城市ID"""
    url = f"https://geoapi.qweather.com/v2/city/lookup?key={api_key}&location={city_name}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == '200' and data.get('location'):
                # 返回第一个匹配的城市ID
                return data['location'][0]['id']
            else:
                print(f"城市查询API错误: {data.get('code')} - 找不到城市: {city_name}")
                return None
        else:
            print(f"城市查询HTTP请求失败: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"城市查询网络请求异常: {e}")
        return None

def get_weather(city_name, api_key):
    """获取指定城市的天气预报 - 使用和风天气API"""
    # 首先获取城市ID
    city_id = get_city_id(city_name, api_key)
    if not city_id:
        return None
    
    # 使用城市ID查询天气
    url = f"https://devapi.qweather.com/v7/weather/now?location={city_id}&key={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == '200':
                # 转换和风天气数据格式为兼容原有逻辑的格式
                weather_info = data['now']
                return {
                    'main': {
                        'temp': float(weather_info['temp']),
                        'feels_like': float(weather_info['feelsLike']),
                        'humidity': int(weather_info['humidity'])
                    },
                    'weather': [{
                        'main': weather_info['text'],
                        'description': weather_info['text']
                    }],
                    'wind': {
                        'speed': float(weather_info['windSpeed']) / 3.6  # 转换 km/h 到 m/s
                    },
                    'visibility': int(weather_info['vis']) * 1000 if weather_info['vis'] != '' else 10000
                }
            else:
                print(f"和风天气API错误: {data.get('code')} - 请检查API密钥")
                return None
        else:
            print(f"天气查询HTTP请求失败: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"天气查询网络请求异常: {e}")
        return None
