# 城市感官探索家 - 贡献指南

感谢您对城市感官探索家项目的关注！我们欢迎任何形式的贡献。

## 如何贡献

### 报告问题

如果您发现了bug或有新的功能建议，请：

1. 检查是否已有相同的问题或建议
2. 如果没有，创建一个新的issue，详细描述问题或建议
3. 提供尽可能多的信息，如复现步骤、错误日志等

### 提交代码

如果您想贡献代码，请遵循以下步骤：

1. Fork本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个Pull Request

### 代码规范

- 遵循PEP 8 Python代码风格指南
- 使用有意义的变量和函数名
- 添加适当的注释和文档字符串
- 保持代码简洁和可读性
- 确保代码通过所有测试

### 提交信息规范

提交信息应该清晰明了，描述您所做的更改。例如：

```
feat: 添加新的天气API接口
fix: 修复地理编码错误
docs: 更新README文档
style: 格式化代码
refactor: 重构数据库模块
test: 添加单元测试
chore: 更新依赖包
```

### 测试

在提交代码之前，请确保：

1. 所有现有测试通过
2. 新功能有相应的测试
3. 代码没有明显的bug

## 项目结构

请参阅[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)了解项目的目录结构和核心文件说明。

## 开发环境设置

1. 克隆仓库：
```bash
git clone https://github.com/your-username/urban-sensory-explorer.git
cd urban-sensory-explorer
```

2. 创建虚拟环境：
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
```bash
cp .env.example .env
# 编辑.env文件，填入你的API密钥
```

5. 运行项目：
```bash
python main.py
```

## 联系方式

如有任何问题或建议，请通过以下方式联系我们：

- 提交issue
- 发送邮件至：your-email@example.com

## 行为准则

- 尊重他人
- 保持友善和专业
- 接受建设性的批评
- 专注于对社区最有利的事情
- 对其他社区成员表示同理心

再次感谢您的贡献！
