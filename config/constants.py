# 全局常量定义

# API相关配置
API_BASE_URL = "https://api.deepseek.com"  # DeepSeek API基础URL
API_TIMEOUT = 60  # 秒
API_RETRY_COUNT = 3

# DeepSeek API配置
DEEPSEEK_API_KEY = "sk-eaa4f9161a724d7fbdf2451c0ff94f00"  # 在此处填入你的DeepSeek API密钥

# 生成相关配置
MAX_CONTENT_LENGTH = 5000  # 字符数
MIN_CONTENT_LENGTH = 100   # 字符数
DEFAULT_LANGUAGE = "zh-CN"

# 文件路径
TEMPLATES_DIR = "data/templates"
LOGS_DIR = "data/logs"

# 日志配置
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"