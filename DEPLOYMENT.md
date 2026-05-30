# 城市感官探索家 - 部署指南

## 本地部署

### 1. 环境准备

确保您的系统已安装以下软件：
- Python 3.8或更高版本
- pip（Python包管理器）

### 2. 克隆项目

```bash
git clone https://github.com/your-username/urban-sensory-explorer.git
cd urban-sensory-explorer
```

### 3. 创建虚拟环境（推荐）

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 配置环境变量

创建`.env`文件，并添加以下内容：

```
AMAP_API_KEY=your_amap_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

### 6. 运行项目

```bash
python main.py
```

### 7. 访问API文档

打开浏览器访问 `http://localhost:8000/docs`

## Docker部署

### 1. 创建Dockerfile

在项目根目录创建`Dockerfile`：

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

### 2. 构建Docker镜像

```bash
docker build -t urban-sensory-explorer .
```

### 3. 运行Docker容器

```bash
docker run -d -p 8000:8000 --env-file .env urban-sensory-explorer
```

### 4. 访问API文档

打开浏览器访问 `http://localhost:8000/docs`

## 云服务部署

### 使用云服务器（如阿里云、腾讯云）

1. 购买云服务器，选择合适的配置（建议2核4G以上）
2. 安装Docker
3. 按照Docker部署步骤进行部署
4. 配置防火墙，开放8000端口
5. 使用Nginx反向代理（可选）

### 使用PaaS平台（如Heroku、Railway）

1. 注册PaaS平台账号
2. 创建新应用
3. 连接代码仓库
4. 配置环境变量
5. 部署应用

## 性能优化

1. 使用缓存减少API调用
2. 使用CDN加速静态资源
3. 使用负载均衡处理高并发
4. 使用数据库连接池
5. 使用异步处理提高响应速度

## 安全建议

1. 不要在代码中硬编码API密钥
2. 使用HTTPS加密通信
3. 实施访问控制和认证
4. 定期更新依赖包
5. 配置防火墙规则
6. 定期备份数据库

## 监控和日志

1. 使用日志记录系统活动
2. 监控API响应时间和错误率
3. 设置警报机制
4. 定期检查系统资源使用情况
