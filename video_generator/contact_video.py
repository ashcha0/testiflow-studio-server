import ffmpeg
from typing import List
import os

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
