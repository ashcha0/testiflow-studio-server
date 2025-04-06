import os
import sys
import logging
from typing import List, Optional
import ffmpeg

# 添加项目根目录到系统路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  

from src.audio_generator.tts_generator import tts_generate
from src.media_search.keyword_extractor import extract_keywords, search_media_by_keywords
from src.utils.logger import setup_logger
from src.video_generator.contact_video import concat_videos, add_audio_to_video

# 设置日志
logger = setup_logger("video_generator")

def generate_video_from_script(
    script: str, 
    narration: str, 
    output_dir: str = "output",
    final_output: str = "final_video.mp4"
) -> str:
    """
    根据脚本和旁白生成完整视频
    
    参数：
        script (str): 视频脚本（用于提取关键词和检索视频素材）
        narration (str): 旁白文案（用于生成语音）
        output_dir (str): 输出目录
        final_output (str): 最终输出文件名
        
    返回：
        str: 最终生成的视频文件路径
    """
    try:
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. 生成语音
        logger.info("开始生成语音...")
        audio_path = os.path.join(output_dir, "narration.mp3")
        audio_path = tts_generate(narration, audio_path)
        logger.info(f"语音生成完成: {audio_path}")
        
        # 2. 提取关键词
        logger.info("开始提取关键词...")
        keywords = extract_keywords(script, top_n=10)
        logger.info(f"提取的关键词: {', '.join(keywords)}")
        
        # 3. 检索媒资
        logger.info("开始检索媒资...")
        video_paths = search_media_by_keywords(keywords)
        if not video_paths:
            logger.error("未找到匹配的视频素材")
            raise ValueError("未找到匹配的视频素材")
        logger.info(f"找到 {len(video_paths)} 个匹配的视频素材")
        
        # 4. 拼接视频
        logger.info("开始拼接视频...")
        concat_output = os.path.join(output_dir, "concat_video.mp4")
        concat_video_path = concat_videos(video_paths, concat_output)
        logger.info(f"视频拼接完成: {concat_video_path}")
        
        # 5. 合成音频和视频
        logger.info("开始合成音频和视频...")
        final_path = os.path.join(output_dir, final_output)
        final_video_path = add_audio_to_video(concat_video_path, audio_path, final_path)
        logger.info(f"音视频合成完成: {final_video_path}")
        
        return final_video_path
    
    except Exception as e:
        logger.error(f"视频生成失败: {str(e)}")
        raise

# 示例用法
if __name__ == "__main__":
    script = """
    这是一个关于自然风景的视频。
    我们将看到美丽的山脉、湖泊和森林。
    大自然的美景令人心旷神怡。
    """
    
    narration = """
    欢迎观看这段自然风景视频。
    大自然的美丽令人叹为观止。
    请欣赏这些壮观的山脉、平静的湖泊和茂密的森林。
    感谢您的观看！
    """
    
    try:
        final_video = generate_video_from_script(script, narration)
        print(f"视频生成完成: {final_video}")
    except Exception as e:
        print(f"视频生成失败: {str(e)}")