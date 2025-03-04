import json
import re
from typing import Dict, List, Any, Union

from config.regex_patterns import HTML_TAG_PATTERN, HASHTAG_PATTERN, MENTION_PATTERN

class ContentParser:
    """解析API返回的内容"""
    
    @staticmethod
    def parse_json_response(response_text: str) -> Dict[str, Any]:
        """解析JSON响应
        
        Args:
            response_text: 响应文本
            
        Returns:
            Dict: 解析后的JSON数据
            
        Raises:
            ValueError: JSON解析错误
        """
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON解析错误: {e}")
    
    @staticmethod
    def extract_main_content(response_data: Dict[str, Any], 
                            content_key: str = "content") -> str:
        """从响应数据中提取主要内容
        
        Args:
            response_data: 响应数据
            content_key: 内容字段名
            
        Returns:
            str: 提取的主要内容
            
        Raises:
            KeyError: 找不到内容字段
        """
        if content_key not in response_data:
            raise KeyError(f"找不到内容字段: {content_key}")
        
        return response_data[content_key]
    
    @staticmethod
    def clean_html_tags(text: str) -> str:
        """清除HTML标签
        
        Args:
            text: 输入文本
            
        Returns:
            str: 清除HTML标签后的文本
        """
        return re.sub(HTML_TAG_PATTERN, '', text)
    
    @staticmethod
    def extract_hashtags(text: str) -> List[str]:
        """提取文本中的话题标签
        
        Args:
            text: 输入文本
            
        Returns:
            List[str]: 提取的话题标签列表
        """
        return re.findall(HASHTAG_PATTERN, text)
    
    @staticmethod
    def extract_mentions(text: str) -> List[str]:
        """提取文本中的@提及
        
        Args:
            text: 输入文本
            
        Returns:
            List[str]: 提取的提及列表
        """
        return re.findall(MENTION_PATTERN, text)
    
    @staticmethod
    def segment_paragraphs(text: str) -> List[str]:
        """将文本分段
        
        Args:
            text: 输入文本
            
        Returns:
            List[str]: 分段后的文本列表
        """
        return [p.strip() for p in text.split('\n') if p.strip()]