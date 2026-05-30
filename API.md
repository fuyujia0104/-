# 城市感官探索家 - API文档

## 基础信息

- 基础URL: `http://localhost:8000`
- API前缀: `/api`
- 数据格式: JSON
- 编码: UTF-8

## 端点列表

### 1. 根路径

**请求**
```
GET /
```

**响应**
```json
{
  "name": "城市感官探索家 API",
  "version": "1.0.0",
  "endpoints": {
    "explore": "/api/explore",
    "search": "/api/search",
    "import_map": "/api/import_map",
    "stream_explore": "/api/stream_explore",
    "mark": "/api/mark"
  }
}
```

### 2. 探索地点感官画像

**请求**
```
GET /api/explore?lat={纬度}&lon={经度}&address={地址（可选）}
```

**参数**
- `lat` (必填): 纬度，浮点数
- `lon` (必填): 经度，浮点数
- `address` (可选): 地址，字符串

**响应**
```json
{
  "location": {
    "address": "地址",
    "latitude": 26.0,
    "longitude": 109.0
  },
  "weather": {
    "condition": "多云",
    "temp": 25,
    "feels_like": 27,
    "humidity": 65,
    "wind_speed": 3.5,
    "wind_direction": 180,
    "visibility": 10,
    "clouds": 30
  },
  "air_quality": {
    "aqi": 50,
    "level": "良",
    "color": "yellow",
    "pm2_5": 25,
    "pm10": 40,
    "o3": 60,
    "no2": 20,
    "so2": 10,
    "co": 0.8
  },
  "noise_level": {
    "decibel": 65,
    "level": "适中",
    "sounds": ["车流声", "人声", "商店音乐"]
  },
  "seasonal_features": ["春光明媚", "百花盛开"],
  "user_marks": [
    {
      "id": 1,
      "mark": "这里的咖啡很香",
      "type": "气味",
      "timestamp": "2024-01-01T12:00:00"
    }
  ],
  "cultural_notes": [
    "这里是老北京胡同文化的重要代表..."
  ]
}
```

### 3. 根据感官偏好搜索地点

**请求**
```
GET /api/search?lat={纬度}&lon={经度}&preferences={偏好}&radius={半径}
```

**参数**
- `lat` (必填): 纬度，浮点数
- `lon` (必填): 经度，浮点数
- `preferences` (必填): 感官偏好，字符串
- `radius` (可选): 搜索半径（公里），默认为5

**响应**
```json
{
  "results": [
    {
      "name": "南山植物园",
      "address": "重庆市南岸区南山公园路101号",
      "latitude": 29.5424,
      "longitude": 106.6337,
      "quietness": 8,
      "weather": "多云",
      "temperature": 26
    }
  ],
  "total": 1
}
```

### 4. 导入GeoJSON地图数据

**请求**
```
POST /api/import_map
Content-Type: multipart/form-data
```

**参数**
- `file` (必填): GeoJSON文件

**响应**
```json
{
  "status": "success",
  "message": "地图数据导入成功",
  "features_count": 10
}
```

### 5. 流式探索体验

**请求**
```
GET /api/stream_explore?lat={纬度}&lon={经度}
```

**参数**
- `lat` (必填): 纬度，浮点数
- `lon` (必填): 经度，浮点数

**响应**
SSE流式响应，每行一个JSON对象：

```
data: {"step": "geocoding", "status": "processing", "message": "正在获取地址信息..."}

data: {"step": "weather", "status": "processing", "message": "正在获取天气信息..."}

data: {"step": "complete", "status": "success", "data": {...}}
```

### 6. 添加用户感官标记

**请求**
```
POST /api/mark
Content-Type: application/json
```

**请求体**
```json
{
  "lat": 26.0,
  "lon": 109.0,
  "mark": "这里的咖啡很香",
  "type": "气味"
}
```

**响应**
```json
{
  "status": "success",
  "message": "标记添加成功",
  "mark_id": 1
}
```

## 错误响应

所有端点在出错时返回以下格式的响应：

```json
{
  "detail": "错误描述信息"
}
```

常见HTTP状态码：
- 200: 成功
- 400: 请求参数错误
- 404: 资源未找到
- 500: 服务器内部错误
