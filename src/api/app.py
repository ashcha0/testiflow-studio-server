import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

from src.script_generator.api_client import APIClient
from src.script_generator.video_script import VideoScriptGenerator
from src.utils.template_loader import TemplateLoader
from config.constants import API_BASE_URL

# 设置日志
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)

# 启用CORS
CORS(app)

# 初始化API客户端
api_client = APIClient(API_BASE_URL)

# 初始化视频脚本生成器
video_script_generator = VideoScriptGenerator(api_client)

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'ok',
        'message': 'Testiflow Studio API服务正常运行'
    })

@app.route('/api/templates', methods=['GET'])
def list_templates():
    """获取所有可用模板"""
    templates = TemplateLoader.list_templates()
    return jsonify({
        'templates': templates
    })

@app.route('/api/templates/<template_name>', methods=['GET'])
def get_template(template_name):
    """获取指定模板内容"""
    template = TemplateLoader.load_template(template_name)
    if not template:
        return jsonify({
            'error': f'模板 {template_name} 不存在'
        }), 404
    
    return jsonify({
        'template': template
    })

@app.route('/api/generate/outline', methods=['POST'])
def generate_outline():
    """生成视频脚本提纲"""
    data = request.json
    if not data or 'title' not in data:
        return jsonify({
            'error': '缺少必要参数: title'
        }), 400
    
    title = data.get('title')
    main_content = data.get('main_content')
    
    try:
        outline = video_script_generator.generate_outline(title, main_content)
        return jsonify(outline)
    except Exception as e:
        logger.error(f"生成提纲失败: {str(e)}")
        return jsonify({
            'error': f'生成提纲失败: {str(e)}'
        }), 500

@app.route('/api/generate/script', methods=['POST'])
def generate_script():
    """生成完整视频脚本"""
    data = request.json
    if not data or 'title' not in data or 'outline' not in data:
        return jsonify({
            'error': '缺少必要参数: title, outline'
        }), 400
    
    title = data.get('title')
    outline = data.get('outline')
    style = data.get('style', '专业')
    tone = data.get('tone', '简洁')
    audience = data.get('audience', '通用')
    
    try:
        script = video_script_generator.generate_script(title, outline, style, tone, audience)
        return jsonify(script)
    except Exception as e:
        logger.error(f"生成脚本失败: {str(e)}")
        return jsonify({
            'error': f'生成脚本失败: {str(e)}'
        }), 500

@app.route('/api/generate/custom', methods=['POST'])
def generate_custom():
    """使用自定义模板生成内容"""
    data = request.json
    if not data or 'template_name' not in data or 'variables' not in data:
        return jsonify({
            'error': '缺少必要参数: template_name, variables'
        }), 400
    
    template_name = data.get('template_name')
    variables = data.get('variables')
    
    # 加载模板
    template = TemplateLoader.load_template(template_name)
    if not template:
        return jsonify({
            'error': f'模板 {template_name} 不存在'
        }), 404
    
    try:
        # 渲染模板
        rendered_template = TemplateLoader.render_template(template, variables)
        
        # 生成内容
        prompt = rendered_template
        if isinstance(rendered_template, str) and rendered_template.startswith("{"):
            import json
            prompt_data = json.loads(rendered_template)
            prompt = prompt_data.get("prompt", rendered_template)
        
        # 调用API
        response = api_client.generate_content(prompt)
        
        return jsonify(response)
    except Exception as e:
        logger.error(f"生成内容失败: {str(e)}")
        return jsonify({
            'error': f'生成内容失败: {str(e)}'
        }), 500

@app.route('/api/outline/save', methods=['POST'])
def save_outline():
    """保存视频脚本提纲"""
    data = request.json
    if not data or 'title' not in data or 'outline' not in data:
        return jsonify({
            'error': '缺少必要参数: title, outline'
        }), 400
    
    title = data.get('title')
    outline = data.get('outline')
    
    try:
        # 确保输出目录存在
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'outputs')
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成文件名
        file_name = f"{title}_outline.json"
        file_path = os.path.join(output_dir, file_name)
        
        # 保存提纲数据
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({'title': title, 'outline': outline}, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'message': '提纲保存成功',
            'file_path': file_path
        })
    except Exception as e:
        logger.error(f"保存提纲失败: {str(e)}")
        return jsonify({
            'error': f'保存提纲失败: {str(e)}'
        }), 500

def create_app():
    """创建并返回Flask应用实例"""
    return app

if __name__ == '__main__':
    # 仅在直接运行此文件时启动服务器
    app.run(debug=True, host='0.0.0.0', port=5000)