# Testiflow Studio 用户指南

## 1. 产品概述

Testiflow Studio 是一款强大的内容生成工具，专注于文案创作和视频脚本生成。通过大模型API集成，提供高质量、定制化的内容输出，满足不同场景的创作需求。

## 2. 已实现功能

### 2.1 文案生成模块

#### 2.1.1 模板系统
- 支持JSON和纯文本格式的模板
- 内置广告文案和文章两种示例模板
- 支持变量插值（使用${variable}语法）
- 模板动态加载和管理

#### 2.1.2 API集成
- 支持与DeepSeek API的对接
- 内置模拟API响应用于开发测试
- 支持API调用重试机制（指数退避策略）
- 可配置的API参数（模型选择、温度等）

#### 2.1.3 内容处理
- 自动分段处理
- HTML标签清理
- 标签（Hashtags）提取
- 提及（Mentions）提取
- 内容质量验证

### 2.2 工具链支持

#### 2.2.1 日志系统
- 分级日志记录
- 控制台实时输出
- 详细的错误追踪

#### 2.2.2 配置管理
- 环境变量支持
- 命令行参数解析
- API密钥管理

#### 2.2.3 文件管理
- 自动创建必要目录
- 模板文件管理
- 输出文件保存

### 2.3 视频脚本生成

#### 2.3.1 提纲生成
- 基于标题和主题生成结构化提纲
- 自动章节划分和描述生成
- 提纲内容解析和格式化

## 3. 使用方法

### 3.1 快速开始

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 创建示例模板：
```bash
python main.py --create-templates
```

3. 使用模拟API测试：
```bash
python main.py --mock
```

4. 设置API密钥：
```bash
python main.py --api-key YOUR_API_KEY
```

5. 生成视频脚本提纲：
```bash
python main.py --video-script --title "人工智能入门指南" --content "介绍AI基础知识和应用场景"
```

### 3.2 模板变量

当前支持的变量列表：

| 变量名 | 说明 | 适用场景 |
|--------|------|----------|
| product | 产品名称 | 广告文案 |
| length | 文案长度 | 广告文案、文章 |
| feature | 产品特点 | 广告文案 |
| audience | 目标受众 | 广告文案、文章 |
| topic | 文章主题 | 文章 |
| type | 文章类型 | 文章 |
| tone | 语气风格 | 广告文案、文章 |
| style | 写作风格 | 文章 |

### 3.3 输出目录结构

```plaintext
testiflow-studio/
├── data/
│   ├── templates/    # 模板文件
│   └── outputs/      # 生成的内容
└── logs/            # 日志文件
```

## 4. 注意事项

### 4.1 模板创建
- JSON模板需包含prompt、model和temperature字段
- 文本模板仅需包含提示词文本
- 模板文件应保存在data/templates/目录下

### 4.2 API使用
- 建议在开发测试时使用--mock参数
- 正式环境需配置有效的API密钥
- API密钥可通过环境变量或命令行参数设置

### 4.3 输出处理
- 内容会自动分段并格式化
- 支持提取标签和提及
- 会进行基础的内容质量验证
- 输出文件默认保存在data/outputs/目录下

## 5. 后续开发计划

### 5.1 视频素材处理模块
- 视频素材检索功能
- 素材库管理
- 关键帧提取

### 5.2 视频合成系统
- 自动字幕生成
- 转场效果支持
- 视频剪辑功能

### 5.3 用户界面优化
- Web界面开发
- 实时预览
- 进度显示

## 6. 常见问题解答

**Q: 如何自定义模板？**  
A: 在data/templates/目录下创建.json或.txt文件，按照示例模板格式编写即可。

**Q: 支持哪些大模型API？**  
A: 目前主要支持DeepSeek API，后续将扩展支持更多模型。

**Q: 如何调整生成内容的质量？**  
A: 可以通过修改模板中的temperature参数（0.1-1.0）来调整，值越低生成内容越稳定，值越高创意性越强。

**Q: 如何生成视频脚本？**  
A: 使用`--video-script`参数，并通过`--title`指定视频标题，可选择通过`--content`提供更详细的内容描述。