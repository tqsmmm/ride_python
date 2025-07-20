
import requests

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
