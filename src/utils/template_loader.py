import os
import json
from typing import Dict, Any, List, Optional
from string import Template

from config.constants import TEMPLATES_DIR

class TemplateLoader:
    """模板加载器，用于加载和渲染提示词模板"""
    
    @staticmethod
    def list_templates() -> List[str]:
        """列出所有可用模板
        
        Returns:
            List[str]: 模板名称列表
        """
        templates_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), TEMPLATES_DIR)
        if not os.path.exists(templates_path):
            return []
        
        return [f.split('.')[0] for f in os.listdir(templates_path) 
                if f.endswith('.json') or f.endswith('.txt')]
    
    @staticmethod
    def load_template(template_name: str) -> Optional[Dict[str, Any]]:
        """加载指定模板
        
        Args:
            template_name: 模板名称
            
        Returns:
            Optional[Dict[str, Any]]: 模板内容，如果模板不存在则返回None
        """
        templates_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), TEMPLATES_DIR)
        
        # 尝试加载JSON模板
        json_path = os.path.join(templates_path, f"{template_name}.json")
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 尝试加载文本模板
        txt_path = os.path.join(templates_path, f"{template_name}.txt")
        if os.path.exists(txt_path):
            with open(txt_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return {"content": content, "type": "text"}
        
        return None
    
    @staticmethod
    def render_template(template_content: Dict[str, Any], variables: Dict[str, Any]) -> str:
        """渲染模板
        
        Args:
            template_content: 模板内容
            variables: 变量字典
            
        Returns:
            str: 渲染后的内容
            
        Raises:
            ValueError: 模板格式错误
        """
        if "type" in template_content and template_content["type"] == "text":
            # 简单文本模板
            template = Template(template_content["content"])
            return template.safe_substitute(variables)
        
        elif "prompt" in template_content:
            # JSON格式模板
            template = Template(template_content["prompt"])
            rendered_prompt = template.safe_substitute(variables)
            
            # 处理可能的其他字段
            result = {
                "prompt": rendered_prompt
            }
            
            # 复制其他非模板字段
            for key, value in template_content.items():
                if key != "prompt":
                    result[key] = value
            
            return json.dumps(result, ensure_ascii=False)
        
        else:
            raise ValueError("无效的模板格式")
    
    @staticmethod
    def save_template(template_name: str, content: str, is_json: bool = False) -> bool:
        """保存模板
        
        Args:
            template_name: 模板名称
            content: 模板内容
            is_json: 是否为JSON格式
            
        Returns:
            bool: 保存是否成功
        """
        templates_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), TEMPLATES_DIR)
        os.makedirs(templates_path, exist_ok=True)
        
        extension = "json" if is_json else "txt"
        file_path = os.path.join(templates_path, f"{template_name}.{extension}")
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception:
            return False