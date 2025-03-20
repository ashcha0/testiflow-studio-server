import os
import sys
import logging
from pathlib import Path

# 设置项目根目录
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.utils.logger import setup_logger
from src.api.app import create_app

# 设置日志
logger = setup_logger("server")

# 创建Flask应用
app = create_app()

if __name__ == '__main__':
    # 获取端口配置，默认为5000
    port = int(os.environ.get('PORT', 5000))
    
    # 启动服务器
    logger.info(f"启动 Testiflow Studio API 服务器，监听端口: {port}")
    app.run(debug=True, host='0.0.0.0', port=port)