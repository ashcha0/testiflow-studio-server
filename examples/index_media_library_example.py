import os
import sys
import logging

# 添加项目根目录到系统路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.media_search.keyword_extractor import index_media_library
from src.utils.logger import setup_logger

# 设置日志
logger = setup_logger("index_media_library_example")

def main():
    # 设置媒资库路径
    media_library_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'media_library'))
    
    # 设置元数据文件名
    metadata_file = "metadata.json"
    
    try:
        logger.info(f"开始为媒资库创建索引: {media_library_path}")
        print(f"开始为媒资库创建索引: {media_library_path}")
        
        # 创建索引
        metadata = index_media_library(media_library_path, metadata_file)
        
        logger.info(f"索引创建成功，共索引了 {len(metadata)} 个视频文件")
        print(f"\n索引创建成功！共索引了 {len(metadata)} 个视频文件")
        print(f"元数据文件保存在: {os.path.join(media_library_path, metadata_file)}")
        
        # 打印索引的内容
        print("\n索引的内容:")
        for item in metadata:
            print(f"文件: {os.path.basename(item['path'])}")
            print(f"标签: {', '.join(item['tags'])}")
            print(f"描述: {item['description']}")
            print("---")
    
    except Exception as e:
        logger.error(f"索引创建失败: {str(e)}")
        print(f"\n索引创建失败: {str(e)}")

if __name__ == "__main__":
    main()