# Testiflow Studio Server

## 1. 项目概述

Testiflow Studio Server 是一个基于Python的内容生成服务端，提供文案创作和视频脚本生成的API服务。项目采用模块化设计，集成大模型API，提供高性能、可扩展的内容生成服务。支持视频脚本提纲生成、完整脚本生成以及数据持久化功能。

## 2. 技术架构

### 2.1 核心技术栈

- **开发语言**: Python 3.8+
- **Web框架**: Flask
- **API集成**: DeepSeek API
- **模板引擎**: Python string.Template
- **日志框架**: Python logging
- **数据库**: SQLite/MySQL

### 2.2 系统架构

```plaintext
testiflow-studio-server/
├── src/                    # 源代码目录
│   ├── api/               # API接口层
│   ├── script_generator/  # 脚本生成模块
│   └── utils/            # 工具类
├── config/                # 配置文件
├── data/                  # 数据目录
│   ├── templates/        # 模板文件
│   ├── outputs/          # 输出文件
│   └── logs/            # 日志文件
└── tests/                # 测试用例
```

## 3. 环境要求与依赖管理

### 3.1 运行环境

- Python 3.8 或更高版本
- pip 包管理工具

### 3.2 依赖安装

```bash
# 安装项目依赖
pip install -r requirements.txt
```

主要依赖包：
- flask==2.0.1
- flask-cors==3.0.10
- python-dotenv==0.19.0
- requests==2.26.0
- sqlalchemy==1.4.23
- ffmpeg-python>=0.2.0

## 4. 快速开始

### 4.1 环境配置

1. 创建并配置环境变量文件：
```bash
cp .env.example .env
```

2. 配置API密钥：
```bash
DEEPSEEK_API_KEY=your_api_key_here
```

### 4.2 启动服务

1. 开发环境启动：
```bash
python run.py
```

2. 生产环境启动：
```bash
python run.py --prod
```

服务默认运行在 http://localhost:5000

## 5. API接口文档

### 5.1 健康检查

```http
GET /api/health
```

**响应示例**：
```json
{
    "status": "ok",
    "message": "Testiflow Studio API服务正常运行"
}
```

### 5.2 模板管理

#### 5.2.1 获取所有模板

```http
GET /api/templates
```

**响应示例**：
```json
{
    "templates": [
        {
            "name": "ad_copy",
            "description": "广告文案模板"
        }
    ]
}
```

#### 5.2.2 获取指定模板

```http
GET /api/templates/{template_name}
```

**响应示例**：
```json
{
    "template": {
        "prompt": "模板内容",
        "model": "deepseek-chat",
        "temperature": 0.7
    }
}
```

### 5.3 视频脚本生成

#### 5.3.1 生成视频脚本提纲

```http
POST /api/generate/outline
Content-Type: application/json

{
    "title": "视频标题",
    "main_content": "视频主要内容描述（可选）"
}
```

**响应示例**：
```json
{
    "title": "视频标题",
    "outline": [
        {
            "title": "第一部分标题",
            "content": "部分内容描述"
        },
        {
            "title": "第二部分标题",
            "content": "部分内容描述"
        }
    ]
}
```

#### 5.3.2 生成完整视频脚本

```http
POST /api/generate/script
Content-Type: application/json

{
    "title": "视频标题",
    "outline": [
        {
            "title": "第一部分标题",
            "content": "部分内容描述"
        }
    ],
    "style": "专业",  // 可选，默认为"专业"
    "tone": "简洁",   // 可选，默认为"简洁"
    "audience": "通用" // 可选，默认为"通用"
}
```

**响应示例**：
```json
{
    "title": "视频标题",
    "script": [
        {
            "section": "第一部分标题",
            "content": "详细脚本内容..."
        }
    ]
}
```

#### 5.3.3 根据提纲ID生成脚本

```http
POST /api/generate/script/{outline_id}
Content-Type: application/json

{
    "style": "专业",  // 可选
    "tone": "简洁",   // 可选
    "audience": "通用" // 可选
}
```

### 5.4 内容生成

#### 5.4.1 使用自定义模板生成内容

```http
POST /api/generate/custom
Content-Type: application/json

{
    "template_name": "ad_copy",
    "variables": {
        "product": "产品名称",
        "feature": "产品特点",
        "audience": "目标受众"
    }
}
```

#### 5.4.2 生成章节内容

```http
POST /api/generate/section
Content-Type: application/json

{
    "title": "章节标题"
}
```

**响应示例**：
```json
{
    "content": "生成的章节详细内容..."
}
```

### 5.5 数据操作

#### 5.5.1 保存提纲

```http
POST /api/outline/save
Content-Type: application/json

{
    "title": "提纲标题",
    "outline": [
        {
            "title": "章节标题",
            "content": "章节内容"
        }
    ]
}
```

**响应示例**：
```json
{
    "message": "提纲保存成功",
    "outline_id": "12345"
}
```

#### 5.5.2 获取数据列表

```http
GET /api/data/list?page=1&size=10
```

**响应示例**：
```json
{
    "data": [
        {
            "id": "12345",
            "title": "提纲标题",
            "created_at": "2023-01-01T12:00:00"
        }
    ],
    "total": 100,
    "page": 1,
    "size": 10
}
```

## 6. 开发指南

### 6.1 项目结构说明

- **api/**: API接口实现
  - `routes/`: 路由定义
  - `models/`: 数据模型
  - `services/`: 业务逻辑

- **script_generator/**: 脚本生成核心模块
  - `generator.py`: 生成器实现
  - `parser.py`: 内容解析器

- **utils/**: 工具类
  - `api_client.py`: API客户端
  - `template_loader.py`: 模板加载器
  - `logger.py`: 日志工具

### 6.2 开发规范

- 遵循PEP 8编码规范
- 使用类型注解
- 编写单元测试
- 使用异步编程模式

### 6.3 测试

```bash
# 运行单元测试
python -m pytest tests/

# 使用模拟API测试
python run.py --mock

# 运行集成测试
python main.py --video-script --title "人工智能入门指南" --content "介绍AI基础知识和应用场景"
```

## 7. 部署说明

### 7.1 Docker部署

```bash
# 构建镜像
docker build -t testiflow-studio-server .

# 运行容器
docker run -d -p 8000:8000 testiflow-studio-server
```

### 7.2 传统部署

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量
3. 启动服务：
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 8. 版本说明

### v1.0.0 (2024-03)
- 初始版本发布
- 支持基础的文案生成功能
- 支持视频脚本提纲生成

### v1.1.0 (计划中)
- 增加更多AI模型支持
- 优化内容生成质量
- 添加批量处理功能

## 9. 常见问题

**Q: 如何处理API调用失败？**  
A: 系统内置了重试机制，默认会进行3次重试，可通过配置文件调整重试策略。

**Q: 如何自定义模板？**  
A: 在`data/templates/`目录下创建JSON格式的模板文件，需包含`prompt`、`model`和`temperature`字段。

**Q: 如何查看API调用日志？**  
A: 日志文件存储在`data/logs/`目录下，按日期分类存储。

## 10. 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交变更
4. 推送到分支
5. 创建Pull Request

## 11. 许可证

本项目采用 MIT 许可证