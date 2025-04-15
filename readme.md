# Testiflow Studio Server 用户手册

## 1. 项目概述

Testiflow Studio Server 是一个基于Python的内容生成服务端，提供文案创作和视频脚本生成的API服务。项目采用模块化设计，集成大模型API，提供高性能、可扩展的内容生成服务。支持视频脚本提纲生成、完整脚本生成以及数据持久化功能。

### 1.1 核心功能

- **视频脚本提纲生成**：根据标题和主要内容生成结构化的视频脚本提纲
- **完整视频脚本生成**：根据提纲生成详细的视频脚本内容
- **自定义模板内容生成**：使用自定义模板和变量生成内容
- **章节内容生成**：根据章节标题生成详细内容
- **数据持久化**：保存和管理生成的提纲和脚本

### 1.2 系统特点

- **模块化设计**：各功能模块职责明确，易于扩展和维护
- **强大的错误处理**：完善的异常处理和重试机制，提高系统稳定性
- **灵活的模板系统**：支持多种格式的模板和变量插值，适应不同场景需求
- **精细的内容处理**：多层次的内容解析和验证，确保输出质量
- **完善的日志系统**：详细的日志记录，便于问题排查和系统监控
- **RESTful API设计**：标准的RESTful API接口，便于集成和调用

## 2. 技术架构

### 2.1 核心技术栈

- **开发语言**: Python 3.13+
- **Web框架**: Flask
- **API集成**: DeepSeek API
- **模板引擎**: Python string.Template
- **日志框架**: Python logging
- **数据库**: SQLite/MySQL
- **ORM框架**: SQLAlchemy
- **跨域支持**: Flask-CORS

### 2.2 系统架构

Testiflow Studio Server 采用模块化设计和分层架构，主要包含以下核心组件：

- **API通信层**：封装与大模型API的交互，处理请求、响应和错误重试
- **内容处理层**：负责解析、验证和格式化生成的内容
- **模板系统**：管理和渲染提示词模板，支持变量插值
- **视频脚本生成器**：生成视频脚本提纲和内容
- **数据库模块**：提供数据持久化和查询功能
- **Web服务层**：提供RESTful API接口
- **工具类**：提供日志、文件管理等通用功能

### 2.3 项目结构

```plaintext
testiflow-studio-server/
├── config/                 # 配置文件目录
│   ├── constants.py        # 全局常量定义
│   └── regex_patterns.py   # 正则表达式模式
├── data/                   # 数据目录
│   ├── logs/               # 日志文件
│   ├── outputs/            # 输出文件
│   └── templates/          # 模板文件
├── src/                    # 源代码目录
│   ├── api/                # API服务模块
│   │   └── app.py          # Flask应用
│   ├── database/           # 数据库模块
│   │   ├── config.py       # 数据库配置
│   │   ├── models.py       # 数据模型
│   │   └── operations.py   # 数据库操作
│   ├── script_generator/   # 脚本生成模块
│   │   ├── api_client.py   # API客户端
│   │   ├── parser.py       # 内容解析器
│   │   ├── validator.py    # 内容验证器
│   │   └── video_script.py # 视频脚本生成器
│   └── utils/              # 工具类
│       ├── logger.py       # 日志工具
│       └── template_loader.py # 模板加载器
├── tests/                  # 测试目录
├── main.py                 # 主程序入口
├── run.py                  # 服务启动脚本
└── requirements.txt        # 依赖包列表
```

## 3. 环境要求与依赖管理

### 3.1 运行环境

- Python 3.13 或更高版本
- pip 包管理工具
- 可选：MySQL数据库（默认使用SQLite）

### 3.2 依赖安装

```bash
# 安装项目依赖
pip install -r requirements.txt
```

主要依赖包：
- flask>=2.0.0
- flask-cors>=3.0.10
- python-dotenv>=0.19.0
- requests>=2.25.1
- sqlalchemy>=1.4.23
- ffmpeg-python>=0.2.0

## 4. 快速开始

### 4.1 环境配置

1. 克隆项目仓库

2. 创建并配置环境变量文件：
```bash
cp .env.example .env
```

3. 配置API密钥：
```bash
DEEPSEEK_API_KEY=your_api_key_here
```

4. 创建必要的目录：
```bash
mkdir -p data/logs data/templates data/outputs
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

### 4.3 使用示例

#### 生成视频脚本提纲

```python
import requests
import json

url = "http://localhost:5000/api/generate/outline"
data = {
    "title": "人工智能在教育领域的应用",
    "main_content": "探讨AI如何改变传统教育模式，提高教学效率和学习体验"
}

response = requests.post(url, json=data)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))
```

#### 保存提纲并生成脚本

```python
import requests
import json

# 1. 生成提纲
outline_url = "http://localhost:5000/api/generate/outline"
outline_data = {
    "title": "人工智能在教育领域的应用",
    "main_content": "探讨AI如何改变传统教育模式，提高教学效率和学习体验"
}

outline_response = requests.post(outline_url, json=outline_data)
outline_result = outline_response.json()

# 2. 保存提纲
save_url = "http://localhost:5000/api/outline/save"
save_data = {
    "title": outline_result["title"],
    "outline": outline_result["outline"]
}

save_response = requests.post(save_url, json=save_data)
save_result = save_response.json()
outline_id = save_result["outline_id"]

# 3. 根据提纲ID生成脚本
script_url = f"http://localhost:5000/api/generate/script/{outline_id}"
script_data = {
    "style": "专业",
    "tone": "简洁",
    "audience": "教育工作者"
}

script_response = requests.post(script_url, json=script_data)
script_result = script_response.json()
print(json.dumps(script_result, indent=2, ensure_ascii=False))
```

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

**路径参数**：

| 参数 | 类型 | 描述 |
|------|------|------|
| template_name | string | 模板名称 |

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

**请求参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| title | string | 是 | 视频标题 |
| main_content | string | 否 | 视频主要内容描述 |

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

#### 5.3.2 根据提纲ID生成脚本

```http
POST /api/generate/script/{outline_id}
Content-Type: application/json

{
    "style": "专业",  
    "tone": "简洁",   
    "audience": "通用" 
}
```

**路径参数**：

| 参数 | 类型 | 描述 |
|------|------|------|
| outline_id | string | 提纲ID或文件路径 |

**请求参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| style | string | 否 | 脚本风格，默认为"专业" |
| tone | string | 否 | 语气风格，默认为"简洁" |
| audience | string | 否 | 目标受众，默认为"通用" |

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

**请求参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| template_name | string | 是 | 模板名称 |
| variables | object | 是 | 模板变量 |

**响应示例**：
```json
{
    "content": "生成的内容..."
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

**请求参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| title | string | 是 | 章节标题 |

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

**请求参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| title | string | 是 | 提纲标题 |
| outline | array | 是 | 提纲内容，包含章节标题和内容 |

**响应示例**：
```json
{
    "message": "提纲保存成功",
    "outline_id": "12345"
}
```

#### 5.5.2 获取提纲列表

```http
GET /api/data/list?page=1&size=10
```

**查询参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| page | integer | 否 | 页码，默认为1 |
| size | integer | 否 | 每页数量，默认为10 |

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

#### 5.5.3 获取提纲详情

```http
GET /api/outline/{outline_id}
```

**路径参数**：

| 参数 | 类型 | 描述 |
|------|------|------|
| outline_id | string | 提纲ID |

**响应示例**：
```json
{
    "title": "提纲标题",
    "outline": [
        {
            "title": "章节标题",
            "content": "章节内容"
        }
    ],
    "created_at": "2023-01-01T12:00:00"
}
```

#### 5.5.4 获取脚本列表

```http
GET /api/script/list?page=1&size=10
```

**查询参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| page | integer | 否 | 页码，默认为1 |
| size | integer | 否 | 每页数量，默认为10 |

**响应示例**：
```json
{
    "data": [
        {
            "id": "12345",
            "outline_id": "67890",
            "outline_title": "提纲标题",
            "created_at": "2023-01-01T12:00:00"
        }
    ],
    "total": 100,
    "page": 1,
    "size": 10
}
```

#### 5.5.5 获取脚本详情

```http
GET /api/script/{script_id}
```

**路径参数**：

| 参数 | 类型 | 描述 |
|------|------|------|
| script_id | string | 脚本ID或提纲ID |

**响应示例**：
```json
{
    "outline_id": "67890",
    "title": "视频标题",
    "content": [
        {
            "section": "第一部分标题",
            "content": "详细脚本内容..."
        }
    ],
    "created_at": "2023-01-01T12:00:00",
    "updated_at": "2023-01-01T12:00:00"
}
```

## 6. 自定义模板开发

### 6.1 模板格式

模板文件支持JSON格式，存放在`data/templates/`目录下。一个典型的模板文件结构如下：

```json
{
    "prompt": "为${product}创建一个针对${audience}的广告文案，突出其${feature}特点。",
    "model": "deepseek-chat",
    "temperature": 0.7,
    "description": "广告文案模板"
}
```

### 6.2 变量插值

模板中的变量使用`${variable}`语法进行标记，在生成内容时会被实际值替换。

### 6.3 创建新模板

1. 在`data/templates/`目录下创建新的JSON文件，如`product_description.json`
2. 定义模板内容，包括prompt、model、temperature等参数
3. 使用API调用模板生成内容

## 7. 开发指南

### 7.1 项目结构说明

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

### 7.2 开发规范

- 遵循PEP 8编码规范
- 使用类型注解
- 编写单元测试
- 使用异步编程模式

### 7.3 测试

```bash
# 运行单元测试
python -m pytest tests/

# 使用模拟API测试
python run.py --mock

# 运行集成测试
python main.py --video-script --title "人工智能入门指南" --content "介绍AI基础知识和应用场景"
```

## 8. 部署说明

### 8.1 Docker部署

```bash
# 构建镜像
docker build -t testiflow-studio-server .

# 运行容器
docker run -d -p 8000:8000 testiflow-studio-server
```

### 8.2 传统部署

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量
3. 启动服务：
```bash
python run.py --prod
```

## 9. 常见问题解答

### 9.1 API调用问题

**Q: 如何处理API调用失败？**  
A: 系统内置了重试机制，默认会进行3次重试，可通过配置文件调整重试策略。如果仍然失败，请检查API密钥是否正确，网络连接是否正常。

**Q: 如何调整API调用的超时时间？**  
A: 在`config/constants.py`文件中修改`API_TIMEOUT`参数，默认为60秒。

### 9.2 内容生成问题

**Q: 如何自定义模板？**  
A: 在`data/templates/`目录下创建JSON格式的模板文件，需包含`prompt`、`model`和`temperature`字段。

**Q: 如何控制生成内容的质量？**  
A: 可以通过调整模板中的temperature参数（0.1-1.0）来控制生成内容的创造性，值越低生成内容越确定性，值越高创造性越强。

### 9.3 系统维护问题

**Q: 如何查看API调用日志？**  
A: 日志文件存储在`data/logs/`目录下，按日期分类存储。

**Q: 如何备份生成的数据？**  
A: 系统使用SQLite或MySQL存储数据，可以使用相应的数据库备份工具进行备份。

## 10. 版本说明

### v1.0.0 (2024-03)
- 初始版本发布
- 支持基础的文案生成功能
- 支持视频脚本提纲生成

### v1.1.0 (计划中)
- 增加更多AI模型支持
- 优化内容生成质量
- 添加批量处理功能

## 11. 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交变更
4. 推送到分支
5. 创建Pull Request

## 12. 许可证

本项目采用 MIT 许可证