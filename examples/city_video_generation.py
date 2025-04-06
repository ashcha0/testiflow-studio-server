import os
import sys
import logging

# 添加项目根目录到系统路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.video_generator.video_generator import generate_video_from_script
from src.utils.logger import setup_logger

# 设置日志
logger = setup_logger("city_video_generation")

def main():
    # 读取城市脚本文件
    script_path = os.path.join(os.path.dirname(__file__), "scripts", "city_script.txt")
    with open(script_path, 'r', encoding='utf-8') as f:
        script = f.read()
    
    # 设置旁白（可以与脚本相同，也可以自定义）
    narration = script
    
    # 设置输出目录
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成视频
    try:
        logger.info("开始生成城市主题视频...")
        final_video = generate_video_from_script(
            script=script,
            narration=narration,
            output_dir=output_dir,
            final_output="final_city_video.mp4"
        )
        logger.info(f"视频生成完成: {final_video}")
        print(f"\n城市主题视频生成成功！输出文件: {final_video}")
    except Exception as e:
        logger.error(f"视频生成失败: {str(e)}")
        print(f"\n视频生成失败: {str(e)}")

if __name__ == "__main__":
    main()