import os
import sys
import logging
import argparse

# 添加项目根目录到系统路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.audio_generator.tts_generator import tts_generate
from src.media_search.keyword_extractor import extract_keywords, search_media_by_keywords, index_media_library
from src.video_generator.contact_video import concat_videos, add_audio_to_video
from src.video_generator.video_generator import generate_video_from_script
from src.utils.logger import setup_logger

# 设置日志
logger = setup_logger("complete_video_generation_workflow")

def process_script(script_path, output_dir, final_output=None, custom_narration=None):
    """
    处理脚本文件并生成视频
    
    参数：
        script_path (str): 脚本文件路径
        output_dir (str): 输出目录
        final_output (str): 最终输出文件名
        custom_narration (str): 自定义旁白文本，如果为None则使用脚本作为旁白
    
    返回：
        str: 生成的视频文件路径
    """
    # 读取脚本文件
    with open(script_path, 'r', encoding='utf-8') as f:
        script = f.read()
    
    # 设置旁白（可以与脚本相同，也可以自定义）
    narration = custom_narration if custom_narration else script
    
    # 设置输出文件名
    if final_output is None:
        script_name = os.path.splitext(os.path.basename(script_path))[0]
        final_output = f"final_{script_name}_video.mp4"
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成视频
    try:
        logger.info(f"开始处理脚本: {script_path}")
        print(f"\n开始处理脚本: {script_path}")
        
        # 1. 提取关键词
        logger.info("提取关键词...")
        keywords = extract_keywords(script, top_n=10)
        logger.info(f"提取的关键词: {', '.join(keywords)}")
        print(f"提取的关键词: {', '.join(keywords)}")
        
        # 2. 生成语音
        logger.info("生成语音...")
        audio_path = os.path.join(output_dir, "narration.mp3")
        audio_path = tts_generate(narration, audio_path)
        logger.info(f"语音生成完成: {audio_path}")
        print(f"语音生成完成: {audio_path}")
        
        # 3. 检索媒资
        logger.info("检索媒资...")
        media_library_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'media_library'))
        video_paths = search_media_by_keywords(keywords, media_library_path)
        logger.info(f"找到 {len(video_paths)} 个匹配的视频素材")
        print(f"找到 {len(video_paths)} 个匹配的视频素材:")
        for path in video_paths:
            print(f"  - {path}")
        
        # 4. 拼接视频
        logger.info("拼接视频...")
        concat_output = os.path.join(output_dir, "concat_video.mp4")
        if video_paths:
            concat_video_path = concat_videos(video_paths, concat_output)
            logger.info(f"视频拼接完成: {concat_video_path}")
            print(f"视频拼接完成: {concat_video_path}")
            
            # 5. 合成音频和视频
            logger.info("合成音频和视频...")
            final_path = os.path.join(output_dir, final_output)
            final_video_path = add_audio_to_video(concat_video_path, audio_path, final_path)
            logger.info(f"音视频合成完成: {final_video_path}")
            print(f"\n视频生成成功！输出文件: {final_video_path}")
            
            return final_video_path
        else:
            logger.error("未找到匹配的视频素材，无法生成视频")
            print("\n未找到匹配的视频素材，无法生成视频")
            print("请确保媒资库中有相关视频素材，或者运行索引脚本更新媒资库索引")
            return None
    
    except Exception as e:
        logger.error(f"视频生成失败: {str(e)}")
        print(f"\n视频生成失败: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(description='视频生成流程示例')
    parser.add_argument('--script', type=str, default=None, 
                        help='脚本文件路径，默认为examples/scripts/city_script.txt')
    parser.add_argument('--narration', type=str, default=None,
                        help='自定义旁白文本文件路径，如果不指定则使用脚本作为旁白')
    parser.add_argument('--output_dir', type=str, default=None,
                        help='输出目录，默认为examples/output')
    parser.add_argument('--output_file', type=str, default=None,
                        help='输出文件名，默认根据脚本名称自动生成')
    parser.add_argument('--index_media', action='store_true',
                        help='是否在生成视频前索引媒资库')
    
    args = parser.parse_args()
    
    # 设置默认值
    if args.script is None:
        args.script = os.path.join(os.path.dirname(__file__), "scripts", "city_script.txt")
    
    if args.output_dir is None:
        args.output_dir = os.path.join(os.path.dirname(__file__), "output")
    
    # 读取自定义旁白（如果有）
    custom_narration = None
    if args.narration:
        with open(args.narration, 'r', encoding='utf-8') as f:
            custom_narration = f.read()
    
    # 索引媒资库（如果需要）
    if args.index_media:
        media_library_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'media_library'))
        logger.info(f"开始为媒资库创建索引: {media_library_path}")
        print(f"开始为媒资库创建索引: {media_library_path}")
        
        metadata = index_media_library(media_library_path)
        logger.info(f"索引创建成功，共索引了 {len(metadata)} 个视频文件")
        print(f"索引创建成功，共索引了 {len(metadata)} 个视频文件")
    
    # 处理脚本并生成视频
    process_script(args.script, args.output_dir, args.output_file, custom_narration)

if __name__ == "__main__":
    main()