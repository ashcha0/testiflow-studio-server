cjh

# Testiflow Studio 功能文档

## 已实现功能

### 1. 文案生成模块

#### 1.1 模板系统
- 支持JSON和纯文本格式的模板
- 内置广告文案和文章两种示例模板
- 支持变量插值（使用${variable}语法）
- 模板动态加载和管理

#### 1.2 API集成
- 支持与大模型API的对接
- 内置模拟API响应用于开发测试
- 支持API调用重试机制
- 可配置的API参数（模型选择、温度等）

#### 1.3 内容处理
- 自动分段处理
- HTML标签清理
- 标签（Hashtags）提取
- 提及（Mentions）提取
- 内容质量验证

### 2. 工具链支持

#### 2.1 日志系统
- 分级日志记录
- 控制台实时输出
- 详细的错误追踪

#### 2.2 配置管理
- 环境变量支持
- 命令行参数解析
- API密钥管理

#### 2.3 文件管理
- 自动创建必要目录
- 模板文件管理
- 输出文件保存

## 使用方法

### 1. 基础命令
```bash
# 创建示例模板
python main.py --create-templates

# 使用模拟API测试
python main.py --mock
# python main.py --create-templates --mock

# 设置API密钥
python main.py --api-key YOUR_API_KEY
```

### 2. 模板变量
当前支持的变量列表：
- product: 产品名称
- length: 文案长度
- feature: 产品特点
- audience: 目标受众
- topic: 文章主题
- type: 文章类型
- tone: 语气风格
- style: 写作风格

### 3. 输出目录结构
```plaintext
testiflow-studio/
├── data/
│   ├── templates/    # 模板文件
│   └── outputs/      # 生成的内容
└── logs/            # 日志文件
```

## 注意事项

1. 模板创建
   - JSON模板需包含prompt、model和temperature字段
   - 文本模板仅需包含提示词文本

2. API使用
   - 建议在开发测试时使用--mock参数
   - 正式环境需配置有效的API密钥

3. 输出处理
   - 内容会自动分段并格式化
   - 支持提取标签和提及
   - 会进行基础的内容质量验证

## 后续开发计划

1. 视频素材处理模块
   - CLIP模型集成
   - ElasticSearch索引
   - 素材库管理

2. 视频合成系统
   - MoviePy工具链
   - 自动字幕生成
   - 转场效果支持

3. 用户界面优化
   - Web界面开发
   - 实时预览
   - 进度显示