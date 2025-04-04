import os
import logging
import json
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
# @app.route('/api/generate/script/<int:script_id>', methods=['POST'])
# def generate_script(script_id=None):
#     """生成完整视频脚本"""
#     if not request.is_json or request.content_type != 'application/json':
#         return jsonify({
#             'error': '请求必须为JSON格式，且Content-Type为application/json',
#             'solution': '请在请求头中添加: Content-Type: application/json'
#         }), 415
        
#     data = request.get_json()
#     if not data or 'title' not in data or 'outline' not in data:
#         return jsonify({
#             'error': '缺少必要参数: title, outline'
#         }), 400
    
#     title = data.get('title')
#     outline = data.get('outline')
#     style = data.get('style', '专业')
#     tone = data.get('tone', '简洁')
#     audience = data.get('audience', '通用')
    
#     try:
#         script = video_script_generator.generate_script(title, outline, style, tone, audience)
#         return jsonify(script)
#     except Exception as e:
#         logger.error(f"生成脚本失败: {str(e)}")
#         return jsonify({
#             'error': f'生成脚本失败: {str(e)}'
#         }), 500

@app.route('/api/generate/script/<path:outline_id>', methods=['POST'])
def generate_script_by_id(outline_id):
    """根据提纲ID生成完整视频脚本"""
    try:
        # 首先尝试从数据库获取提纲
        from src.database.operations import OutlineOperations, ScriptOperations
        from src.database.models import Script
        from datetime import datetime
        import uuid
        
        logger.info(f"开始处理请求，outline_id: {outline_id}")
        data = request.json or {}
        logger.info(f"请求参数: {data}")
        
        # 检查outline_id是否为数字（数据库ID）
        if outline_id.isdigit():
            # 从数据库获取提纲
            outline_obj = OutlineOperations.get_outline_by_id(outline_id)
            if outline_obj:
                logger.info(f"成功获取提纲数据，标题: {outline_obj.title}")
                # 构建提纲数据
                title = outline_obj.title
                outline_sections = [{
                    'title': section.title,
                    'content': section.content
                } for section in outline_obj.sections]
                
                # 获取可选参数
                data = request.json or {}
                style = data.get('style', '专业')
                tone = data.get('tone', '简洁')
                audience = data.get('audience', '通用')
                
                # 生成脚本
                logger.info("开始生成脚本...")
                # 将outline_sections包装在字典中，以符合generate_script方法的期望格式
                outline_dict = {"sections": outline_sections}
                script = video_script_generator.generate_script(title, outline_dict, style, tone, audience)
                logger.info("脚本生成完成")
                
                # 添加ID字段，用于前端跳转
                script['id'] = outline_id
                
                # 保存脚本到数据库
                try:
                    # 检查是否已存在该提纲的脚本
                    existing_script = ScriptOperations.get_script_by_outline(outline_id)
                    script_id = existing_script.script_id if existing_script else str(uuid.uuid4())
                    
                    # 将脚本内容转换为JSON字符串
                    import json
                    script_content = json.dumps(script, ensure_ascii=False)
                    
                    # 创建脚本对象
                    script_obj = Script(
                        script_id=script_id,
                        outline_id=outline_id,
                        content=script_content,
                        created_at=datetime.now()
                    )
                    
                    # 保存到数据库
                    success = ScriptOperations.create_script(script_obj)
                    if success:
                        logger.info(f"脚本保存成功，ID: {script_id}")
                    else:
                        logger.warning(f"脚本保存失败")
                except Exception as e:
                    logger.error(f"保存脚本到数据库失败: {str(e)}")
                
                return jsonify(script)
            else:
                return jsonify({
                    'error': f'提纲不存在: ID {outline_id}'
                }), 404
        
        # 如果不是数字ID，则尝试作为文件路径处理（兼容旧版本）
        if not os.path.exists(outline_id):
            # 尝试在outputs目录中查找
            output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'outputs')
            potential_path = os.path.join(output_dir, os.path.basename(outline_id))
            if os.path.exists(potential_path):
                logger.info(f"找到提纲文件: {potential_path}")
                outline_id = potential_path
            else:
                logger.error(f"提纲文件不存在: {outline_id}")
                return jsonify({
                    'error': f'提纲文件不存在: {outline_id}'
                }), 404
        
        # 读取提纲文件
        with open(outline_id, 'r', encoding='utf-8') as f:
            outline_data = json.load(f)
        
        # 获取标题和提纲
        title = outline_data.get('title')
        outline = outline_data.get('outline')
        
        if not title or not outline:
            return jsonify({
                'error': '提纲文件格式错误，缺少必要字段: title, outline'
            }), 400
        
        # 获取可选参数
        data = request.json or {}
        style = data.get('style', '专业')
        tone = data.get('tone', '简洁')
        audience = data.get('audience', '通用')
        
        # 生成脚本
        script = video_script_generator.generate_script(title, outline, style, tone, audience)
        
        # 添加ID字段，用于前端跳转
        file_id = os.path.basename(outline_id).replace('_outline.json', '')
        script['id'] = file_id
        
        # 保存脚本到数据库
        try:
            from src.database.operations import ScriptOperations
            from src.database.models import Script
            from datetime import datetime
            import uuid
            
            # 生成脚本ID
            script_id = str(uuid.uuid4())
            
            # 将脚本内容转换为JSON字符串
            import json
            script_content = json.dumps(script, ensure_ascii=False)
            
            # 创建脚本对象
            script_obj = Script(
                script_id=script_id,
                outline_id=file_id,  # 使用文件ID作为outline_id
                content=script_content,
                created_at=datetime.now()
            )
            
            # 保存到数据库
            success = ScriptOperations.create_script(script_obj)
            if success:
                logger.info(f"脚本保存成功，ID: {script_id}，提纲ID: {file_id}")
            else:
                logger.warning(f"脚本保存失败")
        except Exception as e:
            logger.error(f"保存脚本到数据库失败: {str(e)}")
        
        return jsonify(script)
    except Exception as e:
        logger.error(f"根据ID生成脚本失败: {str(e)}")
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

@app.route('/api/generate/section', methods=['POST'])
def generate_section_content():
    """生成章节内容"""
    data = request.json
    if not data or 'title' not in data:
        return jsonify({
            'error': '缺少必要参数: title'
        }), 400
    
    title = data.get('title')
    
    try:
        # 构建提示词
        prompt = f"请为标题为《{title}》的视频章节生成详细的内容。内容应该清晰、有条理，并且包含相关的要点和细节。"
        prompt += "\n\n生成的内容应该是一段连贯的文字，不需要包含标题，直接从正文内容开始。"
        
        # 调用API生成内容
        logger.info(f"正在为章节《{title}》生成内容...")
        response = api_client.generate_content(prompt)
        
        # 解析生成的内容
        content = response.get("content", "")
        if not content:
            logger.error("生成章节内容失败，API返回内容为空")
            return jsonify({"error": "生成章节内容失败，请重试"}), 500
        
        return jsonify({"content": content})
    except Exception as e:
        logger.error(f"生成章节内容失败: {str(e)}")
        return jsonify({
            'error': f'生成章节内容失败: {str(e)}'
        }), 500

@app.route('/api/outline/save', methods=['POST'])
def save_outline():
    """保存视频脚本提纲"""
    from src.database.operations import OutlineOperations
    from src.database.models import Outline, OutlineSection
    from datetime import datetime
    
    data = request.json
    if not data or 'title' not in data or 'outline' not in data:
        logger.error("保存提纲失败: 缺少必要参数 title 或 outline")
        return jsonify({
            'error': '缺少必要参数: title, outline'
        }), 400
    
    title = data.get('title')
    outline_sections = data.get('outline')
    outline_id = data.get('id')  # 获取提纲ID，如果存在则更新，否则创建新记录
    
    try:
        # 创建Outline对象
        current_time = datetime.now()
        outline = Outline(
            title=title,
            outline_id=outline_id,  # 设置提纲ID
            sections=[OutlineSection(
                title=section['title'],
                content=section.get('content', '')
            ) for section in outline_sections],
            created_at=current_time,
            updated_at=current_time
        )
        
        logger.info(f"开始保存提纲: {title}")
        
        # 根据是否有outline_id决定创建新记录还是更新现有记录
        if outline_id:
            # 更新现有提纲
            success = OutlineOperations.update_outline(outline)
            if not success:
                logger.error(f"更新提纲失败: 提纲ID {outline_id} 不存在或数据库操作失败")
                raise Exception('更新提纲失败')
                
            logger.info(f"提纲更新成功, ID: {outline_id}")
            return jsonify({
                'message': '提纲更新成功',
                'outline_id': outline_id
            })
        else:
            # 创建新提纲
            new_outline_id = OutlineOperations.create_outline(outline)
            
            if not new_outline_id:
                logger.error("保存提纲失败: 数据库操作返回空ID")
                raise Exception('数据库操作失败')
                
            logger.info(f"提纲保存成功, ID: {new_outline_id}")
            return jsonify({
                'message': '提纲保存成功',
                'outline_id': new_outline_id
            })
    except Exception as e:
        logger.error(f"保存提纲失败: {str(e)}", exc_info=True)
        return jsonify({
            'error': f'保存提纲失败: {str(e)}',
            'details': '请检查数据库连接或联系管理员'
        }), 500

def create_app():
    """创建并返回Flask应用实例"""
    return app

@app.route('/api/data/list', methods=['GET'])
def get_outline_list():
        """获取数据列表"""
        from src.database.operations import OutlineOperations
        
        try:
            page = request.args.get('page', default=1, type=int)
            size = request.args.get('size', default=10, type=int)
            
            # 调用数据库操作方法获取数据
            data = OutlineOperations.get_outline_list(page, size)
            
            return jsonify({
                'data': data['data'],
                'total': data['total'],
                'page': page,
                'size': size
            })
        except Exception as e:
            logger.error(f"获取数据列表失败: {str(e)}")
            return jsonify({
                'error': f'获取数据列表失败: {str(e)}'
            }), 500

@app.route('/api/outline/<outline_id>', methods=['GET'])
def get_outline(outline_id):
    """根据提纲ID获取提纲内容"""
    from src.database.operations import OutlineOperations
    
    try:
        outline = OutlineOperations.get_outline_by_id(outline_id)
        if not outline:
            return jsonify({
                'error': f'获取提纲失败: 提纲ID {outline_id} 不存在'
            }), 404
            
        return jsonify({
            'title': outline.title,
            'outline': [{
                'title': section.title,
                'content': section.content
            } for section in outline.sections],
            'created_at': outline.created_at
        })
    except Exception as e:
        logger.error(f"获取提纲失败: {str(e)}")
        return jsonify({
            'error': f'获取提纲失败: {str(e)}'
        }), 500

@app.route('/api/script/list', methods=['GET'])
def get_script_list():
    """获取脚本列表"""
    from src.database.operations import ScriptOperations
    
    try:
        page = request.args.get('page', default=1, type=int)
        size = request.args.get('size', default=10, type=int)
        
        # 调用数据库操作方法获取脚本列表
        data = ScriptOperations.get_script_list(page, size)
        
        return jsonify({
            'data': data['data'],
            'total': data['total'],
            'page': page,
            'size': size
        })
    except Exception as e:
        logger.error(f"获取脚本列表失败: {str(e)}")
        return jsonify({
            'error': f'获取脚本列表失败: {str(e)}'
        }), 500

@app.route('/api/script/<script_id>', methods=['GET'])
def get_script(script_id):
    """根据脚本ID获取脚本内容"""
    from src.database.operations import ScriptOperations
    import json
    
    try:
        script = ScriptOperations.get_script(script_id)
        if not script:
            return jsonify({
                'error': f'获取脚本失败: 脚本ID {script_id} 不存在'
            }), 404
        
        # 检查脚本内容是否为空
        if not script.content or script.content.strip() == '':
            logger.error(f"脚本内容为空: 脚本ID {script_id}")
            return jsonify({
                'error': f'脚本内容为空或格式不正确'
            }), 500
            
        try:
            # 将JSON字符串转换为Python对象
            script_content = json.loads(script.content)
        except json.JSONDecodeError as json_err:
            logger.error(f"脚本内容JSON解析失败: {str(json_err)}")
            return jsonify({
                'error': f'脚本内容格式不正确，无法解析JSON: {str(json_err)}'
            }), 500
        
        # 确保脚本内容符合预期的JSON格式
        # 处理sections字段，确保它是一个包含content的数组
        sections = script_content.get('sections', [])
        if not isinstance(sections, list):
            sections = []
        
        # 确保每个section都有content字段，并且处理好格式
        processed_sections = []
        for section in sections:
            if not isinstance(section, dict):
                processed_sections.append({"content": str(section)})
            elif "content" not in section:
                section_copy = section.copy()
                section_copy["content"] = ""
                processed_sections.append(section_copy)
            else:
                processed_sections.append(section)
        
        # 更新sections为处理后的数组
        sections = processed_sections
        
        # 构建前端期望的数据结构
        response_data = {
            'outline_id': script.outline_id,
            'title': script_content.get('title', ''),
            'content': sections,
            'created_at': script.created_at,
            'updated_at': script.created_at  # 数据库模型中可能没有updated_at字段，暂用created_at
        }

        # 如果有raw_content字段，也包含在响应中
        if 'raw_content' in script_content:
            response_data['raw_content'] = script_content['raw_content']

        return jsonify(response_data)
    except Exception as e:
        logger.error(f"获取脚本失败: {str(e)}")
        return jsonify({
            'error': f'获取脚本失败: {str(e)}'
        }), 500

if __name__ == '__main__':
    # 仅在直接运行此文件时启动服务器
    app.run(debug=True, host='0.0.0.0', port=5000)