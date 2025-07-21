# 智能骑行建议系统

基于天气条件为你的通勤骑行提供智能建议的Python应用程序。

## 功能特点

- 🌤️ 实时天气数据获取（使用和风天气API）
- 🏠 支持家庭和工作地址的地理编码
- ⚙️ 个性化天气偏好设置
- 🚴‍♂️ 智能骑行建议算法

## 安装和配置

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 获取和风天气API密钥
1. 访问 [和风天气开发平台](https://dev.qweather.com/)
2. 注册账号并登录
3. 创建应用获取API密钥（免费版每天1000次调用）

### 3. 配置文件
复制 `config.json.example` 为 `config.json` 并填入你的信息：

```json
{
  "home_address": "你的家庭地址",
  "work_address": "你的工作地址", 
  "api_key": "你的和风天气API密钥",
  "preferences": {
    "min_temp": 5,        // 最低温度（摄氏度）
    "max_temp": 30,       // 最高温度（摄氏度）
    "max_wind_speed": 10, // 最大风速（m/s）
    "allow_rain": false   // 是否允许雨天骑行
  }
}
```

## 使用方法

```bash
python main.py
```

程序会根据你的家庭地址获取当前天气，并结合你的偏好设置给出骑行建议。

## 技术说明

- **天气API**: 和风天气实时天气API
- **地理编码**: OpenStreetMap Nominatim服务
- **数据格式**: 自动转换和风天气数据为标准格式