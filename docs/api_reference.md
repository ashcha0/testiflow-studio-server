# Testiflow Studio Server API 接口参考文档

## 目录

- [1. 健康检查](#1-健康检查)
- [2. 模板管理](#2-模板管理)
  - [2.1 获取所有模板](#21-获取所有模板)
  - [2.2 获取指定模板](#22-获取指定模板)
- [3. 视频脚本生成](#3-视频脚本生成)
  - [3.1 生成视频脚本提纲](#31-生成视频脚本提纲)
  - [3.2 生成完整视频脚本](#32-生成完整视频脚本)
  - [3.3 根据提纲ID生成脚本](#33-根据提纲id生成脚本)
- [4. 内容生成](#4-内容生成)
  - [4.1 使用自定义模板生成内容](#41-使用自定义模板生成内容)
  - [4.2 生成章节内容](#42-生成章节内容)
- [5. 数据操作](#5-数据操作)
  - [5.1 保存提纲](#51-保存提纲)
  - [5.2 获取数据列表](#52-获取数据列表)

## 1. 健康检查

用于检查API服务是否正常运行。

### 请求

```http
GET /api/health
```

### 响应

```json
{
    "status": "ok",
    "message": "Testiflow Studio API服务正常运行"
}
```

## 2. 模板管理

### 2.1 获取所有模板

获取系统中所有可用的模板列表。

#### 请求

```http
GET /api/templates
```

#### 响应

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

### 2.2 获取指定模板

获取指定名称的模板详细内容。

#### 请求

```http
GET /api/templates/{template_name}
```

**路径参数**：

| 参数 | 类型 | 描述 |
|------|------|------|
| template_name | string | 模板名称 |

#### 响应

**成功响应**：

```json
{
    "template": {
        "prompt": "模板内容",
        "model": "deepseek-chat",
        "temperature": 0.7
    }
}
```

**错误响应**：

```json
{
    "error": "模板 {template_name} 不存在"
}
```

## 3. 视频脚本生成

### 3.1 生成视频脚本提纲

根据标题和主要内容生成视频脚本的提纲。

#### 请求

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

#### 响应

**成功响应**：

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

**错误响应**：

```json
{
    "error": "生成提纲失败: {错误信息}"
}
```

### 3.2 生成完整视频脚本

根据标题和提纲生成完整的视频脚本。

#### 请求

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
    "style": "专业",  
    "tone": "简洁",   
    "audience": "通用" 
}
```

**请求参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| title | string | 是 | 视频标题 |
| outline | array | 是 | 视频提纲，包含章节标题和内容 |
| style | string | 否 | 脚本风格，默认为"专业" |
| tone | string | 否 | 语气风格，默认为"简洁" |
| audience | string | 否 | 目标受众，默认为"通用" |

#### 响应

**成功响应**：

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

**错误响应**：

```json
{
    "error": "生成脚本失败: {错误信息}"
}
```

### 3.3 根据提纲ID生成脚本

根据已保存的提纲ID生成完整视频脚本。

#### 请求

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

#### 响应

与生成完整视频脚本接口相同。

## 4. 内容生成

### 4.1 使用自定义模板生成内容

使用指定的模板和变量生成内容。

#### 请求

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

#### 响应

**成功响应**：

```json
{
    "content": "生成的内容..."
}
```

**错误响应**：

```json
{
    "error": "生成内容失败: {错误信息}"
}
```

### 4.2 生成章节内容

根据章节标题生成详细内容。

#### 请求

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

#### 响应

**成功响应**：

```json
{
    "content": "生成的章节详细内容..."
}
```

**错误响应**：

```json
{
    "error": "生成章节内容失败: {错误信息}"
}
```

## 5. 数据操作

### 5.1 保存提纲

将生成的提纲保存到数据库。

#### 请求

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

#### 响应

**成功响应**：

```json
{
    "message": "提纲保存成功",
    "outline_id": "12345"
}
```

**错误响应**：

```json
{
    "error": "保存提纲失败: {错误信息}",
    "details": "请检查数据库连接或联系管理员"
}
```

### 5.2 获取数据列表

获取已保存的提纲列表，支持分页。

#### 请求

```http
GET /api/data/list?page=1&size=10
```

**查询参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| page | integer | 否 | 页码，默认为1 |
| size | integer | 否 | 每页数量，默认为10 |

#### 响应

**成功响应**：

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

**错误响应**：

```json
{
    "error": "获取数据列表失败: {错误信息}"
}
```
### 5.3 获取提纲

根据提纲ID获取已保存的提纲内容。

#### 请求

```http
GET /api/outline/{outline_id}
```

**路径参数**：

| 参数 | 类型 | 描述 |
|------|------|------|
| outline_id | string | 提纲ID |

#### 响应

**成功响应**：

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

**错误响应**：

```json
{
    "error": "获取提纲失败: {错误信息}"
}
```
