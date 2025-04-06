import ffmpeg
from typing import List, Optional
import os
import sys

# 添加项目根目录到系统路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.audio_generator.tts_generator import tts_generate
from src.media_search.keyword_extractor import extract_keywords, search_media_by_keywords

def concat_videos(video_paths: List[str], output_path: str = "output_dynamic.mp4") -> str:
    """
    将多个视频拼接为一个输出视频。

    参数：
        video_paths (List[str]): 待拼接视频的路径列表
        output_path (str): 输出视频路径（默认 output_dynamic.mp4）

    返回：
        str: 最终输出的视频文件路径
    """
    try:
        # 加载视频和音频流
        inputs = [ffmpeg.input(p) for p in video_paths]
        videos = [i.video.filter('scale', 1920, 1080).filter('fps', fps=30) for i in inputs]
        audios = [i.audio for i in inputs]

        # 拼接视频和音频
        concated = ffmpeg.concat(*[val for pair in zip(videos, audios) for val in pair], v=1, a=1)
        out = concated.output(output_path)

        # 执行合成
        out.run(overwrite_output=True, quiet=True)
        print(f"拼接成功，输出文件为 {output_path}")
        return os.path.abspath(output_path)

    except ffmpeg.Error as e:
        print("FFmpeg 出错了：")
        print(e.stderr.decode('utf8'))
        raise

def add_audio_to_video(video_path: str, audio_path: str, output_path: str = "final_video.mp4") -> str:
    """
    将音频添加到视频中
    
    参数：
        video_path (str): 视频文件路径
        audio_path (str): 音频文件路径
        output_path (str): 输出文件路径
        
    返回：
        str: 最终输出的视频文件路径
    """
    try:
        # 获取视频时长
        probe = ffmpeg.probe(video_path)
        video_duration = float(probe['format']['duration'])
        
        # 获取音频时长
        probe = ffmpeg.probe(audio_path)
        audio_duration = float(probe['format']['duration'])
        
        # 加载视频和音频
        video = ffmpeg.input(video_path)
        audio = ffmpeg.input(audio_path)
        
        # 如果音频比视频长，裁剪音频
        if audio_duration > video_duration:
            audio = audio.filter('atrim', duration=video_duration)
        
        # 如果视频比音频长，循环音频或者调整视频速度
        # 这里选择调整视频速度以匹配音频
        if video_duration > audio_duration:
            speed_factor = video_duration / audio_duration
            video = video.filter('setpts', f'{1/speed_factor}*PTS')
        
        # 合并视频和音频
        out = ffmpeg.output(
            video.video, 
            audio.audio, 
            output_path,
            vcodec='libx264',
            acodec='aac',
            strict='experimental'
        )
        
        # 执行合成
        out.run(overwrite_output=True, quiet=True)
        print(f"音视频合成成功，输出文件为 {output_path}")
        return os.path.abspath(output_path)
        
    except ffmpeg.Error as e:
        print("FFmpeg 出错了：")
        print(e.stderr.decode('utf8'))
        raise
