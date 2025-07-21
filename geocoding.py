
import requests
import re

def get_coordinates(address):
    """将地址转换为经纬度"""
    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json"
    headers = {
        'User-Agent': 'ride-recommender/1.0 (your-email@example.com)'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return float(data['lat']), float(data['lon'])
    else:
        return None, None

def get_city_from_address(address):
    """从地址中提取城市名称"""
    # 中国地址格式通常为：省份+城市+区县+详细地址
    # 使用正则表达式提取城市名称
    
    # 匹配模式：省份名+市名
    city_pattern = r'([^省]+省)?([^市]+市)'
    match = re.search(city_pattern, address)
    
    if match:
        province = match.group(1) if match.group(1) else ""
        city = match.group(2) if match.group(2) else ""
        
        # 去除"省"和"市"字符，只保留名称
        province_name = province.replace('省', '') if province else ""
        city_name = city.replace('市', '') if city else ""
        
        # 对于直辖市，城市名就是省份名
        if city_name in ['北京', '上海', '天津', '重庆']:
            return city_name
        elif province_name in ['北京', '上海', '天津', '重庆']:
            return province_name
        else:
            return city_name if city_name else province_name
    
    # 如果正则匹配失败，尝试简单的字符串分割
    parts = address.split('市')
    if len(parts) > 1:
        # 取第一个"市"前的部分作为城市名
        city_part = parts[0]
        # 去除省份部分
        if '省' in city_part:
            city_part = city_part.split('省')[-1]
        return city_part
    
    # 最后的备选方案，返回地址的前几个字符作为城市标识
    return address[:6] if len(address) >= 6 else address
