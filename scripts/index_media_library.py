import os
import sys
import json
import argparse
from typing import List, Dict, Any

# 添加项目根目录到系统路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.media_search.keyword_extractor import index_media_library
from src.utils.logger import setup_logger

# 设置日志
logger = setup_logger("media_indexer")

def main():
    parser = argparse.ArgumentParser(description='为媒资库创建索引')
    parser.add_argument('--media_path', type=str, default=None, 
                        help='媒资库路径，默认为项目中的media_library目录')
    parser.add_argument('--output', type=str, default='metadata.json',
                        help='输出的元数据文件名，默认为metadata.json')
    
    args = parser.parse_args()
    
    # 如果没有指定媒资库路径，使用默认路径
    if args.media_path is None:
        media_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'media_library'))
    else:
        media_path = os.path.abspath(args.media_path)
    
    # 检查媒资库路径是否存在
    if not os.path.exists(media_path):
        logger.error(f"媒资库路径不存在: {media_path}")
        print(f"错误: 媒资库路径不存在: {media_path}")
        return
    
    try:
        logger.info(f"开始为媒资库创建索引: {media_path}")
        metadata = index_media_library(media_path, args.output)
        logger.info(f"索引创建成功，共索引了 {len(metadata)} 个视频文件")
        print(f"\n索引创建成功！共索引了 {len(metadata)} 个视频文件")
        print(f"元数据文件保存在: {os.path.join(media_path, args.output)}")
    except Exception as e:
        logger.error(f"索引创建失败: {str(e)}")
        print(f"\n索引创建失败: {str(e)}")

if __name__ == "__main__":
    main()