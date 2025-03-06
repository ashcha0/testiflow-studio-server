# Testiflow Studio 开发规划文档

## 1. 技术架构设计

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

- **Python**：服务端逻辑实现
- **JSON**：配置文件和模板定义

### 2.2 关键技术栈

| 功能模块       | 技术方案                          | 说明 |
|----------------|-----------------------------------|--------|
| API通信        | Requests库                        | HTTP客户端，处理与DeepSeek API的通信 |
| 内容处理       | 正则表达式                        | 用于提取和清理生成的内容 |
| 模板系统       | String.Template                   | 支持变量插值的模板引擎 |
| 日志系统       | Python logging                    | 分级日志记录和输出 |
| 配置管理       | 常量模块                          | 集中管理系统配置参数 |

### 2.3 外部依赖

- **DeepSeek API**：用于生成文本内容
- **Requests**：HTTP客户端库

## 3. 开发里程碑计划

### 3.1 阶段性目标

1. **第一阶段**：基础功能实现
   - 文案生成模块开发
   - 模板系统实现
   - API通信层构建

2. **第二阶段**：视频脚本生成
   - 视频脚本提纲生成
   - 内容解析与验证
   - 模拟API响应测试

3. **第三阶段**：功能扩展与优化
   - 多模型支持
   - 批量生成功能
   - 性能优化

## 4. 具体实施步骤

### 4.1 文案生成模块

1. **API客户端开发**：
   ```python
   # api_client.py
   def generate_content(self, prompt: str, params: Dict[str, Any] = None):
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
       # 处理响应...
   ```

2. **模板系统实现**：
   ```python
   # template_loader.py
   def render_template(template_content, variables):
       if "type" in template_content and template_content["type"] == "text":
           template = Template(template_content["content"])
           return template.safe_substitute(variables)
       
       elif "prompt" in template_content:
           template = Template(template_content["prompt"])
           rendered_prompt = template.safe_substitute(variables)
           # 处理其他字段...
   ```

### 4.2 视频脚本生成模块

1. **提纲生成功能**：
   ```python
   # video_script.py
   def generate_outline(self, title, main_content=None):
       # 构建提示词
       prompt = self._build_outline_prompt(title, main_content)
       
       # 调用API生成内容
       response = self.api_client.generate_content(prompt)
       
       # 解析生成的内容
       content = response.get("content", "")
       outline = self._parse_outline(content)
       # 返回结果...
   ```

2. **内容解析实现**：
   ```python
   # parser.py
   def segment_paragraphs(text):
       return [p.strip() for p in text.split('\n') if p.strip()]
       
   def extract_hashtags(text):
       return re.findall(HASHTAG_PATTERN, text)
   ```

### 4.3 测试与优化

1. **模拟API响应**：
   ```python
   # main.py
   def mock_api_response(prompt):
       # 根据不同的提示返回不同的模拟内容
       if "广告文案" in prompt:
           content = """【智能守护，健康随行】..."""
       elif "文章" in prompt:
           content = """# 人工智能：改变我们生活的无形力量..."""
       # 返回模拟响应...
   ```

2. **内容验证**：
   ```python
   # validator.py
   def validate_all(text):
       validations = {
           "length": ContentValidator.validate_length(text),
           "no_sensitive_info": ContentValidator.validate_no_sensitive_info(text),
           "special_chars": ContentValidator.validate_special_chars(text)
       }
       
       all_passed = all(result[0] for result in validations.values())
       # 返回验证结果...
   ```

## 5. 资源需求

- **开发环境**：Python 3.x
- **依赖库**：Requests
- **API资源**：DeepSeek API访问权限
- **存储需求**：模板和输出文件存储

## 6. 关键技术取舍

### 6.1 当前阶段实现

- 文案生成基础功能
- 视频脚本提纲生成
- 模板变量插值系统
- 内容解析与验证

### 6.2 后续阶段规划

- 完整视频脚本生成
- 多模型支持
- 批量生成功能
- Web界面开发

## 7. 技术风险与应对

1. **API稳定性**：实现自动重试机制和错误处理
2. **内容质量**：多层次内容验证和格式化
3. **系统扩展性**：模块化设计，便于后续功能扩展