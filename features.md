# Testiflow Studio Server 功能文档

## 1. 技术架构概述

Testiflow Studio Server 采用模块化设计和分层架构，主要包含以下核心组件：

- **API通信层**：封装与大模型API的交互，处理请求、响应和错误重试
- **内容处理层**：负责解析、验证和格式化生成的内容
- **模板系统**：管理和渲染提示词模板，支持变量插值
- **视频脚本生成器**：生成视频脚本提纲和内容
- **工具类**：提供日志、文件管理等通用功能

### 1.1 系统架构图

```
用户请求 → API客户端 → 大模型API
                ↓
            内容解析器 → 内容验证器
                ↓
            视频脚本生成器 ← 模板加载器
                ↓
              输出结果
```

## 2. 技术选型方案

### 2.1 核心开发语言

- **Python**：主要开发语言，用于服务端逻辑实现
- **JSON**：用于配置文件和模板定义

### 2.2 关键技术栈

| 功能模块 | 技术方案 | 说明 |
|---------|---------|------|
| API通信 | Requests库 | HTTP客户端，处理与大模型API的通信 |
| 内容解析 | 正则表达式 | 用于提取和清理生成的内容 |
| 模板系统 | String.Template | 支持变量插值的模板引擎 |
| 日志系统 | Python logging | 分级日志记录和输出 |
| 配置管理 | 常量模块 | 集中管理系统配置参数 |

### 2.3 外部依赖

- **DeepSeek API**：用于生成文本内容
- **Requests**：HTTP客户端库

## 3. 项目结构

```
testiflow-studio-server/
├── config/                 # 配置文件目录
│   ├── constants.py        # 全局常量定义
│   └── regex_patterns.py   # 正则表达式模式
├── data/                   # 数据目录
│   ├── logs/               # 日志文件
│   ├── outputs/            # 输出文件
│   └── templates/          # 模板文件
├── src/                    # 源代码目录
│   ├── script_generator/   # 脚本生成模块
│   │   ├── api_client.py   # API客户端
│   │   ├── parser.py       # 内容解析器
│   │   ├── validator.py    # 内容验证器
│   │   └── video_script.py # 视频脚本生成器
│   └── utils/              # 工具类
│       ├── logger.py       # 日志工具
│       └── template_loader.py # 模板加载器
├── tests/                  # 测试目录
│   ├── run_tests.py        # 测试运行器
│   ├── test_api_client.py  # API客户端测试
│   └── test_template_loader.py # 模板加载器测试
├── main.py                 # 主程序入口
├── requirements.txt        # 依赖包列表
└── readme.md               # 项目说明文档
```

## 4. 已实现功能模块

### 4.1 API通信模块

#### 4.1.1 APIClient类

提供与大模型API的通信功能，主要特性：

- 支持HTTP请求封装（GET/POST）
- 自动重试机制（指数退避策略）
- 错误处理和日志记录
- 模拟响应模式（用于开发测试）

核心代码示例：

```python
def generate_content(self, prompt: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """生成内容
    
    Args:
        prompt: 提示词
        params: 生成参数
        
    Returns:
        Dict: 生成结果
    """
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        **(params or {})
    }
    
    response = self._make_request('v1/chat/completions', method='POST', data=data)
    
    if not response or 'choices' not in response:
        logger.error(f"API响应格式错误: {response}")
        return {"content": ""}
        
    content = response['choices'][0]['message']['content']
    return {"content": content}
```

### 4.2 内容处理模块

#### 4.2.1 ContentParser类

负责解析和处理API返回的内容，主要功能：

- JSON响应解析
- HTML标签清理
- 标签（Hashtags）提取
- 提及（Mentions）提取
- 内容分段处理

核心代码示例：

```python
@staticmethod
def clean_html_tags(text: str) -> str:
    """清除HTML标签
    
    Args:
        text: 输入文本
        
    Returns:
        str: 清除HTML标签后的文本
    """
    return re.sub(HTML_TAG_PATTERN, '', text)

@staticmethod
def extract_hashtags(text: str) -> List[str]:
    """提取文本中的话题标签
    
    Args:
        text: 输入文本
        
    Returns:
        List[str]: 提取的话题标签列表
    """
    return re.findall(HASHTAG_PATTERN, text)
```

#### 4.2.2 ContentValidator类

验证生成内容的质量和合规性，主要功能：

- 内容长度验证
- 敏感信息检测（邮箱、URL等）
- 特殊字符比例检查
- 综合验证报告生成

### 4.3 模板系统

#### 4.3.1 TemplateLoader类

管理和加载提示词模板，主要功能：

- 支持JSON和纯文本格式的模板
- 模板变量插值（使用${variable}语法）
- 动态模板加载和列表
- 模板保存功能

模板渲染示例：

```python
@staticmethod
def render_template(template_content: Dict[str, Any], variables: Dict[str, Any]) -> str:
    """渲染模板
    
    Args:
        template_content: 模板内容
        variables: 变量字典
        
    Returns:
        str: 渲染后的内容
    """
    if "type" in template_content and template_content["type"] == "text":
        # 简单文本模板
        template = Template(template_content["content"])
        return template.safe_substitute(variables)
    
    elif "prompt" in template_content:
        # JSON格式模板
        template = Template(template_content["prompt"])
        rendered_prompt = template.safe_substitute(variables)
        
        # 处理可能的其他字段
        result = {
            "prompt": rendered_prompt
        }
        
        # 复制其他非模板字段
        for key, value in template_content.items():
            if key != "prompt":
                result[key] = value
        
        return json.dumps(result, ensure_ascii=False)
```

### 4.4 视频脚本生成模块

#### 4.4.1 VideoScriptGenerator类

生成视频脚本提纲和内容，主要功能：

- 生成视频脚本提纲
- 提示词工程优化
- 内容解析和格式化

提示词工程示例：

```python
def _build_outline_prompt(self, title: str, main_content: Optional[str] = None) -> str:
    """构建生成提纲的提示词
    
    Args:
        title: 视频标题/主题
        main_content: 主要内容描述（可选）
        
    Returns:
        str: 构建好的提示词
    """
    prompt = f"请为一个标题为《{title}》的视频脚本生成详细的内容提纲。"
    
    if main_content:
        prompt += f"\n\n视频的主要内容是：{main_content}"
    
    prompt += "\n\n请按照以下格式生成提纲："
    prompt += "\n1. 第一部分标题"
    prompt += "\n   - 这部分应该包含的要点和内容"
    prompt += "\n2. 第二部分标题"
    prompt += "\n   - 这部分应该包含的要点和内容"
    prompt += "\n..."
    
    prompt += "\n\n提纲应该包含3-5个主要部分，每个部分都应该有明确的标题和简短的内容描述。"
    prompt += "\n请确保提纲逻辑清晰，结构合理，能够引导观众从头到尾理解主题。"
    
    return prompt
```

## 5. 技术实现细节

### 5.1 提示词工程

系统采用精心设计的提示词模板，通过明确的指令和格式要求，引导大模型生成结构化的内容。主要技术点：

- 明确的任务描述和要求
- 结构化输出格式指导
- 变量插值实现动态提示词

### 5.2 内容解析与验证

使用正则表达式和结构化解析方法，处理API返回的内容：

- 使用JSON解析器处理结构化响应
- 使用正则表达式提取特定内容（标签、提及等）
- 多重验证确保内容质量和合规性

### 5.3 错误处理与重试

完善的错误处理机制，确保系统稳定性：

- API调用异常捕获和处理
- 自动重试机制（指数退避策略）
- 详细的错误日志记录

## 6. 开发计划

### 6.1 待实现功能

- 完整脚本生成：基于提纲生成完整视频脚本
- 多模型支持：集成更多大模型API
- 批量生成：支持批量生成多个视频脚本
- 内容优化引擎：优化生成内容质量

### 6.2 技术优化

- 性能优化：提高API调用效率和响应速度
- 缓存系统：实现生成结果缓存
- 并发处理：支持并发生成多个内容
- 安全增强：加强API密钥管理和敏感信息处理

## 7. 技术优势

1. **模块化设计**：各功能模块职责明确，易于扩展和维护
2. **强大的错误处理**：完善的异常处理和重试机制，提高系统稳定性
3. **灵活的模板系统**：支持多种格式的模板和变量插值，适应不同场景需求
4. **精细的内容处理**：多层次的内容解析和验证，确保输出质量
5. **完善的日志系统**：详细的日志记录，便于问题排查和系统监控