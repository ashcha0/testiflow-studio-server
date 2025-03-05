import logging
from typing import Dict, List, Any, Optional

from src.script_generator.api_client import APIClient
from src.script_generator.parser import ContentParser
from src.script_generator.validator import ContentValidator

logger = logging.getLogger(__name__)

class VideoScriptGenerator:
    """视频文案脚本生成器，用于生成视频脚本提纲和内容"""
    
    def __init__(self, api_client: APIClient):
        """初始化视频脚本生成器
        
        Args:
            api_client: API客户端实例
        """
        self.api_client = api_client
    
    def generate_outline(self, title: str, main_content: Optional[str] = None) -> Dict[str, Any]:
        """生成视频脚本提纲
        
        Args:
            title: 视频标题/主题
            main_content: 主要内容描述（可选）
            
        Returns:
            Dict: 包含提纲的字典，格式为：
                {
                    "title": "视频标题",
                    "sections": [
                        {"title": "章节1标题", "description": "章节1描述"},
                        {"title": "章节2标题", "description": "章节2描述"},
                        ...
                    ],
                    "raw_content": "原始生成内容"
                }
        """
        # 构建提示词
        prompt = self._build_outline_prompt(title, main_content)
        
        # 调用API生成内容
        logger.info(f"正在为视频《{title}》生成脚本提纲...")
        response = self.api_client.generate_content(prompt)
        
        # 解析生成的内容
        content = response.get("content", "")
        if not content:
            logger.error("生成提纲失败，API返回内容为空")
            return {"error": "生成提纲失败，请重试"}
        
        # 解析提纲结构
        outline = self._parse_outline(content)
        outline["raw_content"] = content
        outline["title"] = title
        
        return outline
    
    def _build_outline_prompt(self, title: str, main_content: Optional[str] = None) -> str:
        """构建生成提纲的提示词
        
        Args:
            title: 视频标题/主题
            main_content: 主要内容描述（可选）
            
        Returns:
            str: 构建好的提示词
        """
        prompt = f"请为一个标题为《{title}》的视频脚本生成详细的内容提纲。"
        
        if main_content:
            prompt += f"\n\n视频的主要内容是：{main_content}"
        
        prompt += "\n\n请按照以下格式生成提纲："
        prompt += "\n1. 第一部分标题"
        prompt += "\n   - 这部分应该包含的要点和内容"
        prompt += "\n2. 第二部分标题"
        prompt += "\n   - 这部分应该包含的要点和内容"
        prompt += "\n..."
        
        prompt += "\n\n提纲应该包含3-5个主要部分，每个部分都应该有明确的标题和简短的内容描述。"
        prompt += "\n请确保提纲逻辑清晰，结构合理，能够引导观众从头到尾理解主题。"
        
        return prompt
    
    def _parse_outline(self, content: str) -> Dict[str, Any]:
        """解析生成的提纲内容
        
        Args:
            content: 生成的原始内容
            
        Returns:
            Dict: 解析后的提纲结构
        """
        # 清理内容
        cleaned_content = ContentParser.clean_html_tags(content)
        
        # 分段处理
        paragraphs = ContentParser.segment_paragraphs(cleaned_content)
        
        # 解析提纲结构
        sections = []
        current_section = None
        description_lines = []
        
        for line in paragraphs:
            # 检查是否是章节标题（数字开头）
            if re.match(r'^\d+\.\s+.+', line):
                # 如果已有章节，保存之前的章节
                if current_section:
                    sections.append({
                        "title": current_section,
                        "description": "\n".join(description_lines)
                    })
                    description_lines = []
                
                # 提取新章节标题
                current_section = line.strip()
            elif current_section and line.strip().startswith('-'):
                # 这是章节的描述点
                description_lines.append(line.strip())
            elif current_section and line.strip() and not line.strip().startswith('#'):
                # 其他内容行，也作为描述
                description_lines.append(line.strip())
        
        # 添加最后一个章节
        if current_section and description_lines:
            sections.append({
                "title": current_section,
                "description": "\n".join(description_lines)
            })
        
        return {"sections": sections}
    
    def generate_full_script(self, outline: Dict[str, Any]) -> Dict[str, Any]:
        """根据提纲生成完整脚本
        
        Args:
            outline: 提纲结构
            
        Returns:
            Dict: 完整脚本内容
        """
        # 这里可以实现根据提纲生成完整脚本的功能
        # 暂时返回一个占位结果
        return {"message": "完整脚本生成功能将在后续版本中实现"}

# 添加必要的导入
import re