
import requests

def get_weather(lat, lon, api_key):
    """获取指定经纬度的天气预报 - 使用和风天气API"""
    # 和风天气实时天气API
    url = f"https://devapi.qweather.com/v7/weather/now?location={lon},{lat}&key={api_key}"
    
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
                print(f"和风天气API错误: {data.get('code')} - 请检查API密钥和请求参数")
                return None
        else:
            print(f"HTTP请求失败: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"网络请求异常: {e}")
        return None
