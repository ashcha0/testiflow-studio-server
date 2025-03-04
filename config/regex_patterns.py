# 正则表达式模板

# 内容验证正则
EMAIL_PATTERN = r'^[\w\.-]+@[\w\.-]+\.\w+$'
URL_PATTERN = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
PHONE_PATTERN = r'(\+\d{1,3})?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'

# 内容提取正则
HASHTAG_PATTERN = r'#(\w+)'
MENTION_PATTERN = r'@(\w+)'

# 内容替换正则
HTML_TAG_PATTERN = r'<[^>]+>'
MULTIPLE_SPACES_PATTERN = r'\s+'

# 特殊字符检测
SPECIAL_CHARS_PATTERN = r'[!@#$%^&*(),.?":{}|<>]'