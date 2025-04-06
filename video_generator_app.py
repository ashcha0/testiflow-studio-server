import os
import sys
import argparse
import logging
from typing import Optional

from src.video_generator.video_generator import generate_video_from_script
from src.media_search.keyword_extractor import index_media_library
from src.utils.logger import setup_logger

# 设置日志
logger = setup_logger("video_generator_app")

def index_media(media_path: Optional[str] = None) -> None:
    """
    为媒资库创建索引
    
    参数：
        media_path (str, optional): 媒资库路径，默认为项目中的media_library目录
    """
    # 如果没有指定媒资库路径，使用默认路径
    if media_path is None:
        media_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'media_library'))
    else:
        media_path = os.path.abspath(media_path)
    
    # 检查媒资库路径是否存在
    if not os.path.exists(media_path):
        logger.error(f"媒资库路径不存在: {media_path}")
        print(f"错误: 媒资库路径不存在: {media_path}")
        return
    
    try:
        logger.info(f"开始为媒资库创建索引: {media_path}")
        metadata = index_media_library(media_path)
        logger.info(f"索引创建成功，共索引了 {len(metadata)} 个视频文件")
        print(f"\n索引创建成功！共索引了 {len(metadata)} 个视频文件")
        print(f"元数据文件保存在: {os.path.join(media_path, 'metadata.json')}")
    except Exception as e:
        logger.error(f"索引创建失败: {str(e)}")
        print(f"\n索引创建失败: {str(e)}")

def generate_video(script: str, narration: str, output_dir: str, output_file: str) -> None:
    """
    根据脚本和旁白生成视频
    
    参数：
        script (str): 视频脚本（用于提取关键词和检索视频素材）
        narration (str): 旁白文案（用于生成语音）
        output_dir (str): 输出目录
        output_file (str): 输出文件名
    """
    try:
        logger.info("开始生成视频...")
        final_video = generate_video_from_script(
            script=script,
            narration=narration,
            output_dir=output_dir,
            final_output=output_file
        )
        logger.info(f"视频生成完成: {final_video}")
        print(f"\n视频生成成功！输出文件: {final_video}")
    except Exception as e:
        logger.error(f"视频生成失败: {str(e)}")
        print(f"\n视频生成失败: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='视频生成系统')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 索引媒资库命令
    index_parser = subparsers.add_parser('index', help='为媒资库创建索引')
    index_parser.add_argument('--media_path', type=str, default=None, 
                             help='媒资库路径，默认为项目中的media_library目录')
    
    # 生成视频命令
    generate_parser = subparsers.add_parser('generate', help='生成视频')
    generate_parser.add_argument('--script', type=str, required=True, 
                                help='视频脚本文件路径')
    generate_parser.add_argument('--narration', type=str, required=True, 
                                help='旁白文案文件路径')
    generate_parser.add_argument('--output_dir', type=str, default='output', 
                                help='输出目录，默认为output')
    generate_parser.add_argument('--output_file', type=str, default='final_video.mp4', 
                                help='输出文件名，默认为final_video.mp4')
    
    args = parser.parse_args()
    
    if args.command == 'index':
        index_media(args.media_path)
    elif args.command == 'generate':
        # 读取脚本和旁白文件
        try:
            with open(args.script, 'r', encoding='utf-8') as f:
                script = f.read()
            
            with open(args.narration, 'r', encoding='utf-8') as f:
                narration = f.read()
            
            # 创建输出目录
            os.makedirs(args.output_dir, exist_ok=True)
            
            # 生成视频
            generate_video(script, narration, args.output_dir, args.output_file)
        except FileNotFoundError as e:
            logger.error(f"文件不存在: {str(e)}")
            print(f"错误: 文件不存在: {str(e)}")
        except Exception as e:
            logger.error(f"发生错误: {str(e)}")
            print(f"错误: {str(e)}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()