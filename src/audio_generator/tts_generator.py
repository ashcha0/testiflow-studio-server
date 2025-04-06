import os
from typing import Optional
import edge_tts  # 使用Edge TTS，免费且效果不错
import asyncio

async def generate_speech(
    text: str, 
    output_path: str = "output_speech.mp3", 
    voice: str = "zh-CN-XiaoxiaoNeural"
) -> str:
    """
    将文本转换为语音文件
    
    参数：
        text (str): 需要转换的文本
        output_path (str): 输出的音频文件路径
        voice (str): 语音角色，默认为微软小晓
        
    返回：
        str: 生成的音频文件的绝对路径
    """
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        print(f"语音生成成功，保存至 {output_path}")
        return os.path.abspath(output_path)
    except Exception as e:
        print(f"语音生成失败: {str(e)}")
        raise

def tts_generate(text: str, output_path: Optional[str] = None) -> str:
    """
    同步调用TTS生成函数的包装器
    """
    if output_path is None:
        output_path = "output_speech.mp3"
    return asyncio.run(generate_speech(text, output_path))