import os
import json
import unittest
import sys
import shutil
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.template_loader import TemplateLoader
from config.constants import TEMPLATES_DIR

class TestTemplateLoader(unittest.TestCase):
    """测试模板加载器功能"""
    
    def setUp(self):
        """测试前准备工作"""
        # 创建临时测试目录
        self.test_templates_dir = os.path.join(os.path.dirname(__file__), 'test_templates')
        os.makedirs(self.test_templates_dir, exist_ok=True)
        
        # 保存原始模板目录路径
        self.original_templates_dir = TEMPLATES_DIR
        
        # 修改模板目录为测试目录
        import config.constants
        config.constants.TEMPLATES_DIR = self.test_templates_dir
        
        # 创建测试模板
        self.create_test_templates()
    
    def tearDown(self):
        """测试后清理工作"""
        # 恢复原始模板目录
        import config.constants
        config.constants.TEMPLATES_DIR = self.original_templates_dir
        
        # 删除测试目录
        if os.path.exists(self.test_templates_dir):
            shutil.rmtree(self.test_templates_dir)
    
    def create_test_templates(self):
        """创建测试用的模板文件"""
        # 创建JSON模板
        json_template = {
            "prompt": "这是一个测试模板，用于${purpose}，包含变量${variable}",
            "model": "gpt-3.5-turbo",
            "temperature": 0.7
        }
        
        with open(os.path.join(self.test_templates_dir, 'test_json.json'), 'w', encoding='utf-8') as f:
            json.dump(json_template, f, ensure_ascii=False)
        
        # 创建文本模板
        with open(os.path.join(self.test_templates_dir, 'test_text.txt'), 'w', encoding='utf-8') as f:
            f.write("这是一个简单的文本模板，用于${purpose}")
    
    def test_list_templates(self):
        """测试列出模板功能"""
        templates = TemplateLoader.list_templates()
        self.assertIn('test_json', templates)
        self.assertIn('test_text', templates)
        self.assertEqual(len(templates), 2)
    
    def test_load_json_template(self):
        """测试加载JSON模板"""
        template = TemplateLoader.load_template('test_json')
        self.assertIsNotNone(template)
        self.assertIn('prompt', template)
        self.assertEqual(template['model'], 'gpt-3.5-turbo')
    
    def test_load_text_template(self):
        """测试加载文本模板"""
        template = TemplateLoader.load_template('test_text')
        self.assertIsNotNone(template)
        self.assertEqual(template['type'], 'text')
        self.assertIn('用于${purpose}', template['content'])
    
    def test_render_json_template(self):
        """测试渲染JSON模板"""
        template = TemplateLoader.load_template('test_json')
        variables = {'purpose': '测试', 'variable': '示例值'}
        rendered = TemplateLoader.render_template(template, variables)
        
        # 解析渲染后的JSON
        rendered_json = json.loads(rendered)
        self.assertIn('测试', rendered_json['prompt'])
        self.assertIn('示例值', rendered_json['prompt'])
        self.assertEqual(rendered_json['model'], 'gpt-3.5-turbo')
    
    def test_render_text_template(self):
        """测试渲染文本模板"""
        template = TemplateLoader.load_template('test_text')
        variables = {'purpose': '单元测试'}
        rendered = TemplateLoader.render_template(template, variables)
        self.assertIn('用于单元测试', rendered)
    
    def test_save_template(self):
        """测试保存模板"""
        # 保存文本模板
        result = TemplateLoader.save_template('new_text', '这是新的${type}模板', is_json=False)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(os.path.join(self.test_templates_dir, 'new_text.txt')))
        
        # 保存JSON模板
        json_content = json.dumps({"prompt": "新的JSON${variable}"})
        result = TemplateLoader.save_template('new_json', json_content, is_json=True)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(os.path.join(self.test_templates_dir, 'new_json.json')))
        
        # 验证新模板可以被加载
        templates = TemplateLoader.list_templates()
        self.assertIn('new_text', templates)
        self.assertIn('new_json', templates)

if __name__ == '__main__':
    unittest.main()