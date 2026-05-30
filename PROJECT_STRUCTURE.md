# 城市感官探索家 - 项目结构说明

## 目录结构

```
城市感官探索家/
├── README.md                 # 项目说明文档
├── LICENSE                   # MIT许可证
├── .gitignore               # Git忽略文件配置
├── .env.example             # 环境变量示例文件
├── requirements.txt         # Python依赖包列表
├── config.py                # 应用配置
├── main.py                  # FastAPI主应用
├── database.py              # 数据库管理模块
├── external_services.py     # 外部服务集成模块
├── knowledge_base.py        # 知识库服务模块
├── data/                    # 数据目录
│   └── sensory_marks.db     # SQLite数据库文件（运行时生成）
├── knowledge_base/          # 知识库目录
│   ├── *.json               # 知识条目文件
├── examples/                # 示例文件目录
│   └── sample_area.geojson  # 示例GeoJSON文件
└── frontend/                # 前端资源目录
    ├── pages/               # 页面文件
    │   └── index.html       # 主页
    ├── services/            # 服务文件
    │   └── api.js           # API服务
    └── styles/              # 样式文件
        └── main.css         # 主样式表
```

## 核心文件说明

### config.py
应用配置文件，包含以下配置项：
- 应用名称和版本
- API前缀
- 服务器配置（主机和端口）
- 高德地图API配置
- OpenWeatherMap API配置
- 数据库路径
- 知识库路径

### main.py
FastAPI主应用文件，定义了以下API端点：
- `/` - 根路径，返回API信息
- `/api/explore` - 探索某个地点的感官画像
- `/api/search` - 根据感官偏好搜索地点
- `/api/import_map` - 导入GeoJSON地图数据
- `/api/stream_explore` - 流式探索体验
- `/api/mark` - 添加用户感官标记

### database.py
数据库管理模块，提供以下功能：
- 数据库初始化
- 感官标记的增删改查
- 标记搜索和过滤

### external_services.py
外部服务集成模块，提供以下功能：
- 高德地图服务（地理编码、逆地理编码、地点搜索）
- 天气服务（获取天气信息、获取空气质量）
- 噪音服务（获取噪音水平）

### knowledge_base.py
知识库服务模块，提供以下功能：
- 知识条目的增删改查
- 知识搜索
- 根据位置获取相关知识

## 环境变量

在项目根目录创建`.env`文件，并配置以下变量：

```
AMAP_API_KEY=your_amap_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

## 运行项目

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量：
```bash
cp .env.example .env
# 编辑.env文件，填入你的API密钥
```

3. 运行项目：
```bash
python main.py
```

4. 访问API文档：
打开浏览器访问 `http://localhost:8000/docs`
