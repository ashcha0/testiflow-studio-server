import re
from typing import List, Dict, Any, Tuple, Optional

from config.constants import MAX_CONTENT_LENGTH, MIN_CONTENT_LENGTH
from config.regex_patterns import SPECIAL_CHARS_PATTERN, EMAIL_PATTERN, URL_PATTERN

class ContentValidator:
    """内容验证器，检查生成内容是否符合要求"""
    
    @staticmethod
    def validate_length(text: str, 
                        min_length: int = MIN_CONTENT_LENGTH, 
                        max_length: int = MAX_CONTENT_LENGTH) -> Tuple[bool, Optional[str]]:
        """验证内容长度
        
        Args:
            text: 待验证文本
            min_length: 最小长度
            max_length: 最大长度
            
        Returns:
            Tuple[bool, Optional[str]]: (是否通过验证, 错误信息)
        """
        if len(text) < min_length:
            return False, f"内容长度({len(text)})小于最小要求({min_length})"
        
        if len(text) > max_length:
            return False, f"内容长度({len(text)})超过最大限制({max_length})"
        
        return True, None
    
    @staticmethod
    def validate_no_sensitive_info(text: str, 
                                  patterns: List[str] = None) -> Tuple[bool, Optional[str]]:
        """验证内容不包含敏感信息
        
        Args:
            text: 待验证文本
            patterns: 敏感信息正则表达式列表
            
        Returns:
            Tuple[bool, Optional[str]]: (是否通过验证, 错误信息)
        """
        if patterns is None:
            patterns = [EMAIL_PATTERN, URL_PATTERN]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                return False, f"内容包含敏感信息: {matches[0]}"
        
        return True, None
    
    @staticmethod
    def validate_special_chars(text: str, 
                              max_special_chars_ratio: float = 0.1) -> Tuple[bool, Optional[str]]:
        """验证特殊字符比例
        
        Args:
            text: 待验证文本
            max_special_chars_ratio: 最大特殊字符比例
            
        Returns:
            Tuple[bool, Optional[str]]: (是否通过验证, 错误信息)
        """
        special_chars = re.findall(SPECIAL_CHARS_PATTERN, text)
        ratio = len(special_chars) / len(text) if text else 0
        
        if ratio > max_special_chars_ratio:
            return False, f"特殊字符比例({ratio:.2f})超过限制({max_special_chars_ratio})"
        
        return True, None
    
    @staticmethod
    def validate_all(text: str) -> Dict[str, Any]:
        """执行所有验证
        
        Args:
            text: 待验证文本
            
        Returns:
            Dict: 验证结果
        """
        validations = {
            "length": ContentValidator.validate_length(text),
            "no_sensitive_info": ContentValidator.validate_no_sensitive_info(text),
            "special_chars": ContentValidator.validate_special_chars(text)
        }
        
        all_passed = all(result[0] for result in validations.values())
        
        return {
            "passed": all_passed,
            "details": {k: {"passed": v[0], "message": v[1]} for k, v in validations.items()}
        }