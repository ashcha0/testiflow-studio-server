import os
import sys
import logging

# 添加项目根目录到系统路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.video_generator.video_generator import generate_video_from_script
from src.utils.logger import setup_logger

# 设置日志
logger = setup_logger("video_generation_example")

def main():
    # 示例脚本和旁白
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
    
    # 设置输出目录
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成视频
    try:
        logger.info("开始生成视频...")
        final_video = generate_video_from_script(
            script=script,
            narration=narration,
            output_dir=output_dir,
            final_output="final_nature_video.mp4"
        )
        logger.info(f"视频生成完成: {final_video}")
        print(f"\n视频生成成功！输出文件: {final_video}")
    except Exception as e:
        logger.error(f"视频生成失败: {str(e)}")
        print(f"\n视频生成失败: {str(e)}")

if __name__ == "__main__":
    main()