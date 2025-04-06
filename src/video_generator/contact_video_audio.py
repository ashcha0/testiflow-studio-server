import ffmpeg
from typing import List
import os
"""
    举个例子便于理解处理逻辑视频V时长34秒，音频A是标准音频，30秒，B，输入为s，20秒，C，输入为r，2，16秒，D，输入为r,0,8秒，最终处理指令为min，则逻辑如下
    
    ABCD先整合A是标准所以ABC的结果是A本身30秒，
    B20秒之后就没有声音了是空白，
    C循环两次是32秒，但是标准是A，所以后两秒删除，也就是先完整一遍，再播放14秒停，
    对于D，他会参照标准音频时长（因为最后其他音频都会对齐到标准）和视频时长谁更长就跟谁，所以视频34秒大于音频30秒，根据视频的34秒他自适应循环，
    他先循环4整遍这时32秒，然后第五遍只有2秒，剩下6秒就删除了，这时得到ABCD整合后的音频时长实际为34秒，
    但裁剪标准是将标准音频的时长与视频时长进行对比，所以是拿A的30秒与视频的34秒进行对比，取min则为30秒，最终处理后视频时长为30秒。

    举一反三，如果音频数据不变传进来一个26秒的视频，则D处理后对齐的是A的30秒最长，所以循环3整遍余6秒，处理后音频时长为30秒，取min则最终输出视频为26秒

"""
def concat_videos_and_audio(video_path: str, audio_paths: List[tuple], standard_audio_path: str, duration_mode: str = 'min', output_path: str = "output_dynamic.mp4") -> str:
    """
    拼接视频和多个音频，音频根据标准音频裁剪或填充，然后拼接生成视频。

    参数：
        video_path (str): 视频文件路径
        audio_paths (List[tuple]): 音频文件路径和音量比率的列表 [(音量比率, 音频路径, 播放方式, 循环次数), ...]
        standard_audio_path (str): 作为标准的音频路径，用于裁剪其他音频
        duration_mode (str): 时长裁剪标准，'min', 'max', 'video', 'audio'
        output_path (str): 输出视频路径

    返回：
        str: 输出视频文件的路径
    """
    # 获取标准音频的时长
    standard_audio_info = ffmpeg.probe(standard_audio_path)
    standard_audio_duration = float(standard_audio_info['streams'][0]['duration'])
    # 获取视频时长
    video_info = ffmpeg.probe(video_path)
    video_duration = float(video_info['streams'][0]['duration'])

    # 音频处理：裁剪或填充音频到标准音频时长
    processed_audio_paths = []
    for i, (volume_ratio, audio_path, play_mode, loop_count) in enumerate(audio_paths):
        # 获取当前音频的时长
        audio_info = ffmpeg.probe(audio_path)
        audio_duration = float(audio_info['streams'][0]['duration'])

        # 根据播放方式和循环次数处理音频
        if play_mode == 's':  # 单次播放
            trimmed_audio = ffmpeg.input(audio_path, ss=0, t=standard_audio_duration)
            trimmed_audio = trimmed_audio.filter('volume', volume_ratio)
        elif play_mode == 'r':  # 循环播放
            if loop_count == 0:  # 自适应循环
                loop_duration = max(standard_audio_duration, video_duration)
                trimmed_audio = ffmpeg.input(audio_path, ss=0, t=loop_duration)
            else:
                trimmed_audio = ffmpeg.input(audio_path, ss=0, t=loop_count * audio_duration)
                trimmed_audio = trimmed_audio.filter('volume', volume_ratio)

        processed_audio_paths.append(trimmed_audio)

    # 拼接音频
    mixed_audio = ffmpeg.concat(*processed_audio_paths, v=0, a=1).node
    audio_out = mixed_audio[0]  # 获取音频输出流

    # 获取视频时长
    video_info = ffmpeg.probe(video_path)
    video_duration = float(video_info['streams'][0]['duration'])

    # 确定最终输出的时长
    if duration_mode == 'min':
        final_duration = min(standard_audio_duration, video_duration)
    elif duration_mode == 'max':
        final_duration = max(standard_audio_duration, video_duration)
    elif duration_mode == 'video':
        final_duration = video_duration
    elif duration_mode == 'audio':
        final_duration = standard_audio_duration

    # 拼接视频和音频
    video = ffmpeg.input(video_path, ss=0, t=final_duration)
    output = ffmpeg.output(video, audio_out, output_path)

    # 执行命令并返回输出路径
    output.run(overwrite_output=True)
    print(f"拼接成功，输出文件为 {output_path}")
    return os.path.abspath(output_path)

# 示例用法
video_file = 'D:/video/clip.mp4'
audio_file_paths = [
    (1, 'D:/audio/audio1.mp3', 's', 1),  # 音频A，音量比率1，时长30秒，单次播放
    (1, 'D:/audio/audio2.mp3', 's', 0),  # 音频B，音量比率1，时长20秒，单次播放
    (1, 'D:/audio/audio3.mp3', 'r', 2),  # 音频C，音量比率1，时长16秒，循环2次
    (1, 'D:/audio/audio4.mp3', 'r', 0)   # 音频D，音量比率1，时长8秒，自适应循环
]
standard_audio_file = 'D:/audio/audio1.mp3'  # 选择音频A作为标准
output_video_path = concat_videos_and_audio(video_file, audio_file_paths, standard_audio_file, 'min', 'output_dynamic.mp4')
print("输出的视频路径：", output_video_path)
