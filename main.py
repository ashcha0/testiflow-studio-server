import os
import sys
import logging
from pathlib import Path

# 设置项目根目录
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.utils.logger import setup_logger
from src.utils.template_loader import TemplateLoader
from src.script_generator.api_client import APIClient
from src.script_generator.parser import ContentParser
from src.script_generator.validator import ContentValidator
from config.constants import API_BASE_URL

# 设置日志
logger = setup_logger("main")

def main():
    """主程序入口"""
    logger.info("启动 testiflow-studio")
    
    # 初始化API客户端
    api_client = APIClient(API_BASE_URL)
    
    # 列出可用模板
    templates = TemplateLoader.list_templates()
    logger.info(f"可用模板: {templates}")
    
    if not templates:
        logger.warning("没有找到可用模板，请先创建模板")
        return
    
    # 选择一个模板
    template_name = templates[0]
    logger.info(f"使用模板: {template_name}")
    
    # 加载模板
    template = TemplateLoader.load_template(template_name)
    if not template:
        logger.error(f"无法加载模板: {template_name}")
        return
    
    # 设置测试变量
    variables = {
        "product": "小米su7 ultra",
        "length": "100",
        "feature": "性价比",
        "audience": "在校大学生",
        "topic": "人工智能",
        "type": "科普",
        "tone": "专业",
        "style": "简洁"
    }
    
    try:
        # 渲染模板
        rendered_template = TemplateLoader.render_template(template, variables)
        logger.info(f"渲染后的模板:\n{rendered_template}")
        
        # 生成内容
        logger.info("正在调用API生成内容...")
        prompt = rendered_template
        if isinstance(rendered_template, str) and rendered_template.startswith("{"):
            import json
            prompt_data = json.loads(rendered_template)
            prompt = prompt_data.get("prompt", rendered_template)
        
        # ======== 新增代码：实际调用API并获取内容 ========
        if os.getenv("USE_MOCK") == "true":
            # 使用模拟响应
            response = mock_api_response(prompt)
        else:
            # 实际调用API
            response = api_client.generate_content(prompt)
        
        # 从响应中提取内容
        content = response.get("content", "")
        # ======== 新增代码结束 ========
        
        # 解析内容
        logger.info("解析生成的内容...")
        if isinstance(content, dict) and "content" in content:
            parsed_content = ContentParser.extract_main_content(content)
        else:
            parsed_content = content
        cleaned_content = ContentParser.clean_html_tags(parsed_content)
        
        # 分段处理
        paragraphs = ContentParser.segment_paragraphs(cleaned_content)
        
        # 提取标签和提及
        hashtags = ContentParser.extract_hashtags(cleaned_content)
        mentions = ContentParser.extract_mentions(cleaned_content)
        
        # 验证内容
        logger.info("验证内容质量...")
        validation_result = ContentValidator.validate_all(cleaned_content)
        
        if validation_result["passed"]:
            logger.info("内容验证通过")
            
            # 输出生成的内容
            logger.info("生成的内容:")
            for i, para in enumerate(paragraphs):
                logger.info(f"段落 {i+1}: {para}")
            
            if hashtags:
                logger.info(f"提取的标签: {hashtags}")
            
            if mentions:
                logger.info(f"提取的提及: {mentions}")
                
            # 保存结果
            output_dir = os.path.join(project_root, "data", "outputs")
            os.makedirs(output_dir, exist_ok=True)
            
            output_file = os.path.join(output_dir, f"{template_name}_output.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n\n".join(paragraphs))
            
            logger.info(f"内容已保存到: {output_file}")
        else:
            logger.warning("内容验证失败")
            for key, detail in validation_result["details"].items():
                if not detail["passed"]:
                    logger.warning(f"- {key}: {detail['message']}")
            
    except Exception as e:
        logger.error(f"生成过程出错: {str(e)}")
        import traceback
        logger.debug(traceback.format_exc())

def mock_api_response(prompt):
    """模拟API响应，用于测试"""
    logger.info(f"模拟API请求: {prompt}")
    
    # 根据不同的提示返回不同的模拟内容
    if "广告文案" in prompt:
        content = """
        【智能守护，健康随行】
        
        忙碌的工作日，你的健康谁来守护？智能手表，24小时实时监测心率、血氧、睡眠质量，智能分析健康数据，及时预警异常。轻薄设计，长效续航，贴合职场人士需求。健康，从腕间开始，让每一天都充满活力！#健康监测 #智能手表 @年轻上班族
        """
    elif "文章" in prompt:
        content = """
        # 人工智能：改变我们生活的无形力量
        
        人工智能(AI)正以前所未有的速度融入我们的日常生活。从智能手机上的语音助手到自动驾驶汽车，AI技术正在悄然改变我们与世界互动的方式。
        
        ## 什么是人工智能？
        
        简单来说，人工智能是让机器模拟人类智能的科学。它通过复杂算法和大量数据学习，不断提升自身能力。
        
        ## AI的应用领域
        
        医疗领域中，AI可以辅助诊断疾病，提高准确率；在金融行业，AI能够预测市场趋势，优化投资决策；在教育方面，AI可以根据学生特点提供个性化学习方案。
        
        ## 未来展望
        
        随着技术不断发展，AI将更加智能化、人性化。但同时，我们也需要思考AI带来的伦理问题和社会影响。
        
        人工智能不是未来，而是已经融入当下。了解并适应这一技术革命，将帮助我们更好地迎接智能时代的到来。
        
        #人工智能 #科技发展 @科技爱好者
        """
    else:
        content = """
        这是一个模拟的API响应内容。
        
        您的提示是：
        
        {}
        
        由于这只是一个测试响应，内容比较简单。在实际应用中，这里会返回由AI生成的更加丰富和相关的内容。
        
        #测试 #模拟
        """.format(prompt)
    
    # 返回一个包含content字段的字典，模拟API响应结构
    return {"content": content, "status": "success", "model": "mock-model"}
def create_sample_templates():
    """创建示例模板"""
    templates_dir = os.path.join(project_root, "data", "templates")
    os.makedirs(templates_dir, exist_ok=True)
    
    # 广告文案模板
    ad_template = {
        "prompt": "请为${product}编写一段${length}字的广告文案，突出其${feature}特点，目标受众是${audience}。",
        "model": "gpt-3.5-turbo",
        "temperature": 0.7
    }
    
    # 文章模板
    article_template = "我需要一篇关于${topic}的${type}文章，字数在500左右，风格要${style}，语调要${tone}。"
    
    # 保存模板
    TemplateLoader.save_template("ad_copy", json.dumps(ad_template, ensure_ascii=False), is_json=True)
    TemplateLoader.save_template("article", article_template, is_json=False)
    
    logger.info("示例模板已创建")

if __name__ == "__main__":
    import json
    import argparse
    
    parser = argparse.ArgumentParser(description="Testiflow Studio - 文案生成工具")
    parser.add_argument("--create-templates", action="store_true", help="创建示例模板")
    parser.add_argument("--api-key", type=str, help="设置API密钥")
    parser.add_argument("--mock", action="store_true", help="使用模拟API响应进行测试")
    args = parser.parse_args()
    
    if args.create_templates:
        create_sample_templates()
    
    if args.api_key:
        # 设置API密钥
        os.environ["API_KEY"] = args.api_key
        logger.info("API密钥已设置")
    
    if args.mock:
        # 启用模拟模式
        os.environ["USE_MOCK"] = "true"
        logger.info("已启用模拟API模式")
    
    main()
