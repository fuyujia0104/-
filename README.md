
# 城市感官探索家 (Urban Sensory Explorer)

城市感官探索家是一个融合了现代科技与人文情怀的城市探索向导系统，通过整合实时环境数据、地图服务、用户感官标记和城市文化知识库，为用户提供更人性化、更立体的地点推荐与探索体验。

## 功能特点

1. **地点感官画像**：根据坐标或地址，获取地点的综合感官信息，包括天气、空气质量、噪音水平、季节性特征等。
2. **感官需求搜索**：根据用户的感官偏好（安静、气味、氛围等）搜索合适的地点。
3. **区域感官普查**：导入GeoJSON地图数据，对指定区域进行感官特征分析。
4. **流式探索体验**：通过SSE实时推送探索进度，提供更丰富的交互体验。
5. **用户感官标记**：允许用户添加地点的感官标记，构建共享的感官记忆库。
6. **文化知识库**：整合城市历史文化信息，为推荐提供文化背景。

## 技术架构

- **后端框架**：FastAPI
- **数据库**：SQLite
- **外部API**：
  - 高德地图API（地理编码、地点搜索）
  - OpenWeatherMap API（天气、空气质量）
- **通信协议**：HTTP/SSE

## 快速开始

1. 克隆项目仓库：
```bash
git clone https://github.com/your-username/urban-sensory-explorer.git
cd urban-sensory-explorer
```

2. 创建虚拟环境（推荐）：
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
创建`.env`文件，并添加以下内容：
```
AMAP_API_KEY=your_amap_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

5. 运行项目：
```bash
python main.py
```

6. 访问API文档：
打开浏览器访问 `http://localhost:8000/docs`

编辑`.env`文件，填入你的API密钥：
```
AMAP_API_KEY=your_amap_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

5. 运行应用：
```bash
python -m uvicorn main:app --reload
```

应用将在`http://localhost:8000`启动。

## API端点

### 1. 探索地点感官画像

**请求**：
```
GET /api/explore?lat=39.917&lon=116.417&address=北新桥头条胡同
```

**响应**：
```json
{
  "location": "北新桥头条胡同",
  "coordinates": {
    "latitude": 39.917,
    "longitude": 116.417
  },
  "weather": {
    "condition": "晴",
    "temp": 22,
    "feels_like": 21,
    "humidity": 45,
    "wind": "2.5 m/s"
  },
  "air_quality": {
    "aqi": 35,
    "level": "优",
    "pm2_5": 12
  },
  "noise": {
    "level": "安静",
    "decibel": 42,
    "sounds": ["鸟鸣", "远处车流声"]
  },
  "seasonal_features": ["桂花香", "银杏叶黄"],
  "user_marks": ["安静4星，适合看书"],
  "cultural_notes": ["这里曾是元代漕运码头..."]
}
```

### 2. 按感官需求搜索地点

**请求**：
```
GET /api/search?lat=39.917&lon=116.417&preferences=quiet,no_smell,study&radius=2.0
```

**响应**：
```json
{
  "center": {
    "latitude": 39.917,
    "longitude": 116.417
  },
  "radius": 2.0,
  "preferences": "quiet,no_smell,study",
  "results": [
    {
      "name": "氧气咖啡",
      "address": "五道营胡同12号",
      "coordinates": {
        "latitude": 39.918,
        "longitude": 116.418
      },
      "type": "咖啡厅",
      "weather": {
        "condition": "晴",
        "temp": 22
      },
      "air_quality": {
        "aqi": 35,
        "level": "优"
      },
      "noise": {
        "level": "安静",
        "sounds": ["轻音乐", "低语声"]
      },
      "seasonal_features": ["桂花香", "银杏叶黄"],
      "user_marks": {
        "quietness": 4,
        "smells": ["咖啡香"],
        "atmospheres": ["安静", "文艺"]
      },
      "cultural_notes": ["五道营胡同原是明代兵营..."],
      "match_score": 5
    }
  ]
}
```

### 3. 导入地图数据

**请求**：
```
POST /api/import_map
Content-Type: application/json

{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [116.4, 39.9],
            [116.5, 39.9],
            [116.5, 40.0],
            [116.4, 40.0],
            [116.4, 39.9]
          ]
        ]
      },
      "properties": {
        "name": "南锣鼓巷区域"
      }
    }
  ]
}
```

**响应**：
```json
{
  "area_bounds": {
    "min_lat": 39.9,
    "max_lat": 40.0,
    "min_lon": 116.4,
    "max_lon": 116.5
  },
  "area_summary": {
    "mark_count": 5,
    "avg_quietness": 3.8,
    "common_smells": ["咖啡", "烤面包"],
    "best_season": "秋季",
    "summary": "此区域共有5个用户标记点，整体安静程度3.8星，常见气味：咖啡、烤面包，最佳季节：秋季"
  },
  "center_point": {
    "latitude": 39.95,
    "longitude": 116.45,
    "address": "北京市东城区南锣鼓巷"
  },
  "current_conditions": {
    "weather": {
      "condition": "晴",
      "temp": 22
    },
    "air_quality": {
      "aqi": 35,
      "level": "优"
    }
  },
  "cultural_notes": ["南锣鼓巷的历史典故..."]
}
```

### 4. SSE流式探索

**请求**：
```
GET /api/stream_explore?lat=39.917&lon=116.417
```

**响应**（SSE流）：
```
data: {"step": "location", "status": "获取位置信息中..."}

data: {"step": "location", "status": "位置: 北京市东城区北新桥头条胡同"}

data: {"step": "weather", "status": "获取天气中..."}

data: {"step": "weather", "status": "天气：晴，温度22°C"}

data: {"step": "aqi", "status": "空气质量良好(AQI: 35)"}

data: {"step": "noise", "status": "噪音水平：安静"}

data: {"step": "culture", "content": "这里曾是元代漕运码头..."}

data: {"step": "done", "summary": "综合推荐：您可以去氧气咖啡，评分4.2/5"}
```

### 5. 添加用户感官标记

**请求**：
```
POST /api/mark
Content-Type: application/json

{
  "latitude": 39.917,
  "longitude": 116.417,
  "address": "北新桥头条胡同",
  "quietness": 4,
  "smell": "咖啡香",
  "atmosphere": "安静",
  "best_season": "秋季",
  "best_time_of_day": "下午",
  "notes": "安静4星，适合看书"
}
```

**响应**：
```json
{
  "success": true,
  "message": "感官标记已添加",
  "mark_id": 1
}
```

## API文档

启动应用后，可以通过以下地址访问API文档：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 项目结构

```
城市感官探索家/
├── main.py                 # FastAPI应用主文件
├── config.py               # 配置文件
├── database.py             # 数据库操作
├── external_services.py    # 外部API服务
├── knowledge_base.py       # 知识库服务
├── requirements.txt        # 项目依赖
├── .env.example           # 环境变量模板
├── README.md              # 项目说明
├── data/                  # 数据目录
│   └── sensory_marks.db   # SQLite数据库
└── knowledge_base/        # 知识库目录
    └── *.json             # 知识条目
```

## 知识库扩展

要添加新的城市文化知识，可以编辑`knowledge_base.py`文件中的`_add_sample_data`方法，或者通过API添加新的知识条目。

## 许可证

MIT License

## 贡献

欢迎提交问题报告和拉取请求！
