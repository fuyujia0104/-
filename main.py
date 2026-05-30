from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
import json
import asyncio
from datetime import datetime

from config import settings
from database import DatabaseManager
from external_services import AmapService, WeatherService, NoiseService
from knowledge_base import KnowledgeBaseService

# 初始化应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="城市感官探索家API - 提供地点感官画像、搜索和知识库服务"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化服务
db = DatabaseManager()
amap_service = AmapService()
weather_service = WeatherService()
noise_service = NoiseService()
kb_service = KnowledgeBaseService()

@app.get("/")
async def root():
    """根路径，返回API信息"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "endpoints": {
            "explore": f"{settings.API_PREFIX}/explore",
            "search": f"{settings.API_PREFIX}/search",
            "import_map": f"{settings.API_PREFIX}/import_map",
            "stream_explore": f"{settings.API_PREFIX}/stream_explore",
            "mark": f"{settings.API_PREFIX}/mark"
        }
    }

@app.get(f"{settings.API_PREFIX}/explore")
async def explore(
    lat: float = Query(..., description="纬度"),
    lon: float = Query(..., description="经度"),
    address: Optional[str] = Query(None, description="地址（可选）")
):
    """
    探索某个地点的感官画像

    根据坐标或地址，获取该点的综合感官信息，包括：
    - 天气情况
    - 空气质量
    - 附近声音
    - 季节性特征
    - 用户标记
    - 文化笔记
    """
    try:
        print(f"Starting explore for lat={lat}, lon={lon}, address={address}")
        # 如果提供了地址但未提供坐标，则进行地理编码
        if address and (lat is None or lon is None):
            print("Geocoding address...")
            location = await amap_service.geocode(address)
            if location:
                lat = location["latitude"]
                lon = location["longitude"]
                print(f"Geocoded to lat={lat}, lon={lon}")

        # 如果未提供地址，则进行逆地理编码
        if not address:
            print("Reverse geocoding...")
            geocode_data = await amap_service.reverse_geocode(lat, lon)
            if geocode_data:
                address = geocode_data.get("address", "")
                print(f"Reverse geocoded to address={address}")

        # 获取天气信息
        print("Getting weather...")
        weather = await weather_service.get_weather(lat, lon)
        print(f"Weather: {weather}")

        # 获取空气质量
        print("Getting air quality...")
        air_quality = await weather_service.get_air_quality(lat, lon)
        print(f"Air quality: {air_quality}")

        # 获取噪音水平
        print("Getting noise level...")
        noise_level = await noise_service.get_noise_level(lat, lon)
        print(f"Noise level: {noise_level}")

        # 获取季节性特征
        print("Getting seasonal features...")
        seasonal_features = await weather_service.get_seasonal_features(lat, lon)
        print(f"Seasonal features: {seasonal_features}")

        # 获取用户标记
        print("Getting user marks...")
        user_marks = db.get_nearby_marks(lat, lon)
        user_marks_summary = [mark["notes"] for mark in user_marks[:5]]
        print(f"User marks: {user_marks_summary}")

        # 获取文化笔记
        print("Getting cultural notes...")
        cultural_notes = kb_service.get_related_knowledge(address, lat, lon)
        print(f"Cultural notes: {cultural_notes}")

        return {
            "location": address,
            "coordinates": {
                "latitude": lat,
                "longitude": lon
            },
            "weather": {
                "condition": weather.get("condition", "未知"),
                "temp": weather.get("temp", 0),
                "feels_like": weather.get("feels_like", 0),
                "humidity": weather.get("humidity", 0),
                "wind": f"{weather.get('wind_speed', 0)} m/s"
            },
            "air_quality": {
                "aqi": air_quality.get("aqi", 0),
                "level": air_quality.get("level", "未知"),
                "pm2_5": air_quality.get("pm2_5", 0)
            },
            "noise": {
                "level": noise_level.get("level", "未知"),
                "decibel": noise_level.get("decibel", 0),
                "sounds": noise_level.get("sounds", [])
            },
            "seasonal_features": seasonal_features,
            "user_marks": user_marks_summary,
            "cultural_notes": cultural_notes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get(f"{settings.API_PREFIX}/search")
async def search(
    lat: float = Query(..., description="中心点纬度"),
    lon: float = Query(..., description="中心点经度"),
    preferences: Optional[str] = Query(None, description="感官偏好，逗号分隔，如：quiet,no_smell,study"),
    radius: float = Query(2.0, description="搜索半径（公里）")
):
    """
    按感官需求搜索地点

    在指定中心点附近，寻找满足感官偏好的地点
    """
    try:
        # 解析偏好参数
        pref_dict = {}
        if preferences:
            for pref in preferences.split(","):
                pref = pref.strip().lower()
                if pref == "quiet":
                    pref_dict["quietness"] = 4  # 安静程度至少4星
                elif pref == "no_smell":
                    pref_dict["smell"] = "无"
                elif pref == "study":
                    pref_dict["atmosphere"] = "安静"

        # 搜索地点
        places = db.get_places_by_sensory_preferences(
            lat=lat,
            lon=lon,
            radius_km=radius,
            preferences=pref_dict
        )

        # 为每个地点获取更多感官信息
        results = []
        for place in places:
            place_lat = place["latitude"]
            place_lon = place["longitude"]

            # 获取天气信息
            weather = await weather_service.get_weather(place_lat, place_lon)

            # 获取空气质量
            air_quality = await weather_service.get_air_quality(place_lat, place_lon)

            # 获取噪音水平
            noise_level = await noise_service.get_noise_level(place_lat, place_lon)

            # 获取季节性特征
            seasonal_features = await weather_service.get_seasonal_features(place_lat, place_lon)

            # 获取文化笔记
            cultural_notes = kb_service.get_related_knowledge(place["name"], place_lat, place_lon)

            # 计算匹配度（简单示例）
            match_score = 0
            if "quietness" in pref_dict and place.get("avg_quietness", 0) >= pref_dict["quietness"]:
                match_score += 3
            if "smell" in pref_dict and pref_dict["smell"] in place.get("smells", []):
                match_score += 2
            if "atmosphere" in pref_dict and pref_dict["atmosphere"] in place.get("atmospheres", []):
                match_score += 2

            results.append({
                "name": place["name"],
                "address": place["address"],
                "coordinates": {
                    "latitude": place_lat,
                    "longitude": place_lon
                },
                "type": place["place_type"],
                "weather": {
                    "condition": weather.get("condition", "未知"),
                    "temp": weather.get("temp", 0)
                },
                "air_quality": {
                    "aqi": air_quality.get("aqi", 0),
                    "level": air_quality.get("level", "未知")
                },
                "noise": {
                    "level": noise_level.get("level", "未知"),
                    "sounds": noise_level.get("sounds", [])
                },
                "seasonal_features": seasonal_features,
                "user_marks": {
                    "quietness": place.get("avg_quietness", 0),
                    "smells": place.get("smells", []),
                    "atmospheres": place.get("atmospheres", [])
                },
                "cultural_notes": cultural_notes,
                "match_score": match_score
            })

        # 按匹配度排序
        results.sort(key=lambda x: x["match_score"], reverse=True)

        return {
            "center": {
                "latitude": lat,
                "longitude": lon
            },
            "radius": radius,
            "preferences": preferences,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post(f"{settings.API_PREFIX}/import_map")
async def import_map(
    geojson: Dict[str, Any] = Body(..., description="GeoJSON格式的地图数据")
):
    """
    导入地图数据并进行区域分析

    接收用户上传的GeoJSON文件，对区域进行感官普查
    """
    try:
        # 提取边界框
        bounds = {
            "min_lat": float("inf"),
            "max_lat": float("-inf"),
            "min_lon": float("inf"),
            "max_lon": float("-inf")
        }

        # 解析GeoJSON并计算边界框
        if "features" in geojson:
            for feature in geojson["features"]:
                geometry = feature.get("geometry", {})
                if geometry.get("type") == "Polygon":
                    coordinates = geometry.get("coordinates", [])
                    if coordinates:
                        for point in coordinates[0]:
                            lon, lat = point[0], point[1]
                            bounds["min_lat"] = min(bounds["min_lat"], lat)
                            bounds["max_lat"] = max(bounds["max_lat"], lat)
                            bounds["min_lon"] = min(bounds["min_lon"], lon)
                            bounds["max_lon"] = max(bounds["max_lon"], lon)
                elif geometry.get("type") == "Point":
                    coordinates = geometry.get("coordinates", [])
                    if coordinates:
                        lon, lat = coordinates[0], coordinates[1]
                        bounds["min_lat"] = min(bounds["min_lat"], lat)
                        bounds["max_lat"] = max(bounds["max_lat"], lat)
                        bounds["min_lon"] = min(bounds["min_lon"], lon)
                        bounds["max_lon"] = max(bounds["max_lon"], lon)

        # 如果没有有效的边界框，返回错误
        if bounds["min_lat"] == float("inf"):
            raise HTTPException(status_code=400, detail="无效的GeoJSON数据")

        # 获取区域摘要
        area_summary = db.get_area_summary(bounds)

        # 计算中心点
        center_lat = (bounds["min_lat"] + bounds["max_lat"]) / 2
        center_lon = (bounds["min_lon"] + bounds["max_lon"]) / 2

        # 获取中心点的天气和空气质量
        weather = await weather_service.get_weather(center_lat, center_lon)
        air_quality = await weather_service.get_air_quality(center_lat, center_lon)

        # 获取文化笔记
        address = await amap_service.reverse_geocode(center_lat, center_lon)
        cultural_notes = kb_service.get_related_knowledge(address.get("address", ""), center_lat, center_lon)

        return {
            "area_bounds": bounds,
            "area_summary": area_summary,
            "center_point": {
                "latitude": center_lat,
                "longitude": center_lon,
                "address": address.get("address", "")
            },
            "current_conditions": {
                "weather": {
                    "condition": weather.get("condition", "未知"),
                    "temp": weather.get("temp", 0)
                },
                "air_quality": {
                    "aqi": air_quality.get("aqi", 0),
                    "level": air_quality.get("level", "未知")
                }
            },
            "cultural_notes": cultural_notes
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get(f"{settings.API_PREFIX}/stream_explore")
async def stream_explore(
    lat: float = Query(..., description="纬度"),
    lon: float = Query(..., description="经度")
):
    """
    SSE流式探索

    通过SSE实时推送探索进度，适合大范围分析
    """
    async def event_generator():
        try:
            # 1. 获取位置信息
            yield f"data: {json.dumps({'step': 'location', 'status': '获取位置信息中...'}, ensure_ascii=False)}\n\n"

            geocode_data = await amap_service.reverse_geocode(lat, lon)
            address = geocode_data.get("address", "")
            yield f"data: {json.dumps({'step': 'location', 'status': f'位置: {address}'}, ensure_ascii=False)}\n\n"

            # 2. 获取天气信息
            yield f"data: {json.dumps({'step': 'weather', 'status': '获取天气中...'}, ensure_ascii=False)}\n\n"
            weather = await weather_service.get_weather(lat, lon)
            weather_desc = f"天气：{weather.get('condition', '未知')}，温度{weather.get('temp', 0)}°C"
            yield f"data: {json.dumps({'step': 'weather', 'status': weather_desc}, ensure_ascii=False)}\n\n"

            # 3. 获取空气质量
            yield f"data: {json.dumps({'step': 'aqi', 'status': '获取空气质量中...'}, ensure_ascii=False)}\n\n"
            air_quality = await weather_service.get_air_quality(lat, lon)
            aqi_desc = f"空气质量：{air_quality.get('level', '未知')}(AQI: {air_quality.get('aqi', 0)})"
            yield f"data: {json.dumps({'step': 'aqi', 'status': aqi_desc}, ensure_ascii=False)}\n\n"

            # 4. 获取噪音水平
            yield f"data: {json.dumps({'step': 'noise', 'status': '获取噪音水平中...'}, ensure_ascii=False)}\n\n"
            noise_level = await noise_service.get_noise_level(lat, lon)
            noise_desc = f"噪音水平：{noise_level.get('level', '未知')}({noise_level.get('decibel', 0)}分贝)"
            yield f"data: {json.dumps({'step': 'noise', 'status': noise_desc}, ensure_ascii=False)}\n\n"

            # 5. 获取季节性特征
            yield f"data: {json.dumps({'step': 'seasonal', 'status': '获取季节性特征中...'}, ensure_ascii=False)}\n\n"
            seasonal_features = await weather_service.get_seasonal_features(lat, lon)
            seasonal_desc = "季节特征：" + "、".join(seasonal_features)
            yield f"data: {json.dumps({'step': 'seasonal', 'status': seasonal_desc}, ensure_ascii=False)}\n\n"

            # 6. 获取用户标记
            yield f"data: {json.dumps({'step': 'marks', 'status': '获取用户标记中...'}, ensure_ascii=False)}\n\n"
            user_marks = db.get_nearby_marks(lat, lon)
            marks_count = len(user_marks)
            marks_desc = f"发现{marks_count}处用户标记"
            yield f"data: {json.dumps({'step': 'marks', 'status': marks_desc}, ensure_ascii=False)}\n\n"

            # 7. 获取文化笔记
            yield f"data: {json.dumps({'step': 'culture', 'status': '获取文化知识中...'}, ensure_ascii=False)}\n\n"
            cultural_notes = kb_service.get_related_knowledge(address, lat, lon)

            # 逐条发送文化笔记
            for i, note in enumerate(cultural_notes):
                yield f"data: {json.dumps({'step': 'culture', 'content': note}, ensure_ascii=False)}\n\n"


            # 8. 生成综合推荐
            yield f"data: {json.dumps({'step': 'summary', 'status': '生成综合推荐中...'}, ensure_ascii=False)}\n\n"

            # 简单的推荐逻辑
            if marks_count > 0:
                best_mark = user_marks[0]
                recommendation = f"根据用户标记，推荐您前往{address}附近，这里被评价为'{best_mark.get('notes', '未知')}'"
            else:
                recommendation = f"根据环境数据，{address}当前天气{weather.get('condition', '未知')}，空气{air_quality.get('level', '未知')}，适合户外活动"

            # 完成探索
            yield f"data: {json.dumps({'step': 'done', 'summary': recommendation}, ensure_ascii=False)}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'step': 'error', 'message': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@app.post(f"{settings.API_PREFIX}/mark")
async def add_mark(
    mark_data: Dict[str, Any] = Body(..., description="感官标记数据")
):
    """
    添加用户感官标记

    保存用户提交的感官标签，存入本地数据库
    """
    try:
        # 验证必要字段
        if "latitude" not in mark_data or "longitude" not in mark_data:
            raise HTTPException(status_code=400, detail="缺少必要字段: latitude, longitude")

        # 如果未提供地址，则进行逆地理编码
        if "address" not in mark_data or not mark_data["address"]:
            geocode_data = await amap_service.reverse_geocode(
                mark_data["latitude"],
                mark_data["longitude"]
            )
            mark_data["address"] = geocode_data.get("address", "")

        # 添加标记到数据库
        mark_id = db.add_sensory_mark(mark_data)

        # 可选：将标记添加到知识库
        if mark_data.get("notes"):
            kb_service.add_knowledge(
                title=f"用户标记: {mark_data.get('address', '未知位置')}",
                content=mark_data.get("notes", ""),
                tags=["用户标记", mark_data.get("atmosphere", ""), mark_data.get("smell", "")]
            )

        return {
            "success": True,
            "message": "感官标记已添加",
            "mark_id": mark_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
