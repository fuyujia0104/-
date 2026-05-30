
import httpx
from typing import Dict, List, Optional, Any
from config import settings

class AmapService:
    """高德地图API服务"""

    def __init__(self):
        self.api_key = settings.AMAP_API_KEY
        self.base_url = settings.AMAP_BASE_URL

    async def reverse_geocode(self, lat: float, lon: float) -> Dict[str, Any]:
        """逆地理编码：根据坐标获取地址信息"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/geocode/regeo",
                    params={
                        "key": self.api_key,
                        "location": f"{lon},{lat}",
                        "extensions": "all",
                        "output": "json"
                    }
                )
                data = response.json()

                if data["status"] == "1":
                    regeocode = data.get("regeocode", {})
                    return {
                        "address": regeocode.get("formatted_address", ""),
                        "province": regeocode.get("addressComponent", {}).get("province", ""),
                        "city": regeocode.get("addressComponent", {}).get("city", ""),
                        "district": regeocode.get("addressComponent", {}).get("district", ""),
                        "street": regeocode.get("addressComponent", {}).get("street", {}).get("street", ""),
                        "pois": [poi.get("name", "") for poi in regeocode.get("pois", [])[:5]]
                    }
                return {
                    "address": "",
                    "province": "",
                    "city": "",
                    "district": "",
                    "street": "",
                    "pois": []
                }
        except Exception as e:
            print(f"Error in reverse_geocode: {e}")
            return {
                "address": "",
                "province": "",
                "city": "",
                "district": "",
                "street": "",
                "pois": []
            }

    async def search_places(self, keywords: str, city: str = None, 
                           lat: float = None, lon: float = None, 
                           radius: int = 2000) -> List[Dict[str, Any]]:
        """地点搜索"""
        async with httpx.AsyncClient() as client:
            params = {
                "key": self.api_key,
                "keywords": keywords,
                "output": "json"
            }

            if city:
                params["city"] = city

            if lat and lon:
                params["location"] = f"{lon},{lat}"
                params["radius"] = radius

            response = await client.get(
                f"{self.base_url}/place/around",
                params=params
            )
            data = response.json()

            if data["status"] == "1":
                pois = data.get("pois", [])
                return [
                    {
                        "name": poi.get("name", ""),
                        "address": poi.get("address", ""),
                        "location": poi.get("location", "").split(","),
                        "type": poi.get("type", ""),
                        "distance": poi.get("distance", 0)
                    }
                    for poi in pois[:20]
                ]
            return []

    async def geocode(self, address: str, city: str = None) -> Optional[Dict[str, Any]]:
        """地理编码：根据地址获取坐标"""
        async with httpx.AsyncClient() as client:
            params = {
                "key": self.api_key,
                "address": address,
                "output": "json"
            }

            if city:
                params["city"] = city

            response = await client.get(
                f"{self.base_url}/geocode/geo",
                params=params
            )
            data = response.json()

            if data["status"] == "1":
                geocodes = data.get("geocodes", [])
                if geocodes:
                    location = geocodes[0].get("location", "").split(",")
                    if len(location) == 2:
                        return {
                            "longitude": float(location[0]),
                            "latitude": float(location[1]),
                            "formatted_address": geocodes[0].get("formatted_address", "")
                        }
            return None


class WeatherService:
    """天气和空气质量API服务"""

    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = settings.OPENWEATHER_BASE_URL
        self.air_pollution_url = settings.OPENWEATHER_AIR_POLLUTION_URL

    async def get_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        """获取天气信息"""
        try:
            async with httpx.AsyncClient(timeout=30.0, verify=False) as client:
                response = await client.get(
                    self.base_url,
                    params={
                        "lat": lat,
                        "lon": lon,
                        "appid": self.api_key,
                        "units": "metric",
                        "lang": "zh_cn"
                    }
                )
                data = response.json()
        except Exception as e:
            print(f"Error getting weather: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return {
                "condition": "未知",
                "temp": 0,
                "feels_like": 0,
                "humidity": 0,
                "wind_speed": 0,
                "wind_direction": 0,
                "visibility": 0,
                "clouds": 0
            }

            if "weather" in data:
                weather = data.get("weather", [{}])[0]
                main = data.get("main", {})
                wind = data.get("wind", {})
                clouds = data.get("clouds", {})

                return {
                    "condition": weather.get("description", "未知"),
                    "temp": main.get("temp", 0),
                    "feels_like": main.get("feels_like", 0),
                    "humidity": main.get("humidity", 0),
                    "wind_speed": wind.get("speed", 0),
                    "wind_direction": wind.get("deg", 0),
                    "visibility": data.get("visibility", 0) / 1000,  # 转换为公里
                    "clouds": clouds.get("all", 0)
                }
            return {
                "condition": "未知",
                "temp": 0,
                "feels_like": 0,
                "humidity": 0,
                "wind_speed": 0,
                "wind_direction": 0,
                "visibility": 0,
                "clouds": 0
            }

    async def get_air_quality(self, lat: float, lon: float) -> Dict[str, Any]:
        """获取空气质量信息"""
        try:
            async with httpx.AsyncClient(timeout=30.0, verify=False) as client:
                response = await client.get(
                    self.air_pollution_url,
                    params={
                        "lat": lat,
                        "lon": lon,
                        "appid": self.api_key
                    }
                )
                data = response.json()

                if "list" in data and len(data["list"]) > 0:
                    aqi_data = data["list"][0]
                    components = aqi_data.get("components", {})
                    aqi = aqi_data.get("main", {}).get("aqi", 0)

                    # AQI等级划分
                    if aqi <= 50:
                        level = "优"
                        color = "green"
                    elif aqi <= 100:
                        level = "良"
                        color = "yellow"
                    elif aqi <= 150:
                        level = "轻度污染"
                        color = "orange"
                    elif aqi <= 200:
                        level = "中度污染"
                        color = "red"
                    elif aqi <= 300:
                        level = "重度污染"
                        color = "purple"
                    else:
                        level = "严重污染"
                        color = "maroon"

                    return {
                        "aqi": int(aqi),
                        "level": level,
                        "color": color,
                        "pm2_5": components.get("pm2_5", 0),
                    "pm10": components.get("pm10", 0),
                    "o3": components.get("o3", 0),
                    "no2": components.get("no2", 0),
                    "so2": components.get("so2", 0),
                    "co": components.get("co", 0)
                }
            return {
                "aqi": 0,
                "level": "未知",
                "color": "gray",
                "pm2_5": 0,
                "pm10": 0,
                "o3": 0,
                "no2": 0,
                "so2": 0,
                "co": 0
            }
        except Exception as e:
            print(f"Error getting air quality: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return {
                "aqi": 0,
                "level": "未知",
                "color": "gray",
                "pm2_5": 0,
                "pm10": 0,
                "o3": 0,
                "no2": 0,
                "so2": 0,
                "co": 0
            }

    async def get_seasonal_features(self, lat: float, lon: float) -> List[str]:
        """根据当前季节和位置获取季节性特征"""
        import datetime

        weather = await self.get_weather(lat, lon)
        temp = weather.get("temp", 0)

        # 获取当前月份
        month = datetime.datetime.now().month

        seasonal_features = []

        # 根据月份和温度判断季节性特征
        if 3 <= month <= 5:  # 春季
            if temp > 10:
                seasonal_features.append("春花盛开")
            if temp < 20:
                seasonal_features.append("春寒料峭")
            seasonal_features.append("春光明媚")
        elif 6 <= month <= 8:  # 夏季
            if temp > 30:
                seasonal_features.append("炎热")
            else:
                seasonal_features.append("温暖")
            seasonal_features.append("绿树成荫")
        elif 9 <= month <= 11:  # 秋季
            if temp < 20:
                seasonal_features.append("秋高气爽")
            if month == 10:
                seasonal_features.append("桂花香")
            if month == 11:
                seasonal_features.append("银杏叶黄")
        else:  # 冬季
            if temp < 0:
                seasonal_features.append("寒冷")
            elif temp < 10:
                seasonal_features.append("微寒")
            else:
                seasonal_features.append("温和")
            if month == 12 or month == 1:
                seasonal_features.append("冬日阳光")

        return seasonal_features


class NoiseService:
    """噪音数据服务"""

    def __init__(self):
        # 这里可以集成实际的噪音API，目前使用模拟数据
        pass

    async def get_noise_level(self, lat: float, lon: float) -> Dict[str, Any]:
        """获取指定位置的噪音水平"""
        import random

        # 模拟噪音数据，实际应用中应该从噪音API获取
        base_noise = random.randint(30, 70)

        # 根据时间调整噪音水平
        import datetime
        hour = datetime.datetime.now().hour

        if 7 <= hour <= 9 or 17 <= hour <= 19:  # 早晚高峰
            base_noise += 15
        elif 22 <= hour or hour <= 6:  # 夜间
            base_noise -= 15

        # 确保噪音水平在合理范围内
        base_noise = max(20, min(90, base_noise))

        # 噪音等级描述
        if base_noise < 40:
            level = "非常安静"
            sounds = ["鸟鸣", "风吹树叶声"]
        elif base_noise < 55:
            level = "安静"
            sounds = ["远处车流声", "人声"]
        elif base_noise < 70:
            level = "适中"
            sounds = ["车流声", "人声", "商店音乐"]
        else:
            level = "喧闹"
            sounds = ["车流声", "人声", "施工声", "商店音乐"]

        return {
            "decibel": base_noise,
            "level": level,
            "sounds": sounds
        }
