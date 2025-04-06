import jieba.analyse
from typing import List, Dict, Any
import os
import json
import glob

def extract_keywords(script: str, top_n: int = 5) -> List[str]:
    """
    从脚本中提取关键词
    
    参数：
        script (str): 脚本文本
        top_n (int): 提取的关键词数量
        
    返回：
        List[str]: 关键词列表
    """
    # 使用jieba提取关键词
    keywords = jieba.analyse.extract_tags(script, topK=top_n)
    return keywords

def search_media_by_keywords(
    keywords: List[str], 
    media_library_path: str = "d:\\14730\\Desktop\\GitProject\\testiflow-studio\\media_library",
    metadata_file: str = "metadata.json"
) -> List[str]:
    """
    根据关键词在媒资库中检索相关视频
    
    参数：
        keywords (List[str]): 关键词列表
        media_library_path (str): 媒资库路径
        metadata_file (str): 媒资元数据文件
        
    返回：
        List[str]: 匹配的视频文件路径列表
    """
    # 加载媒资库元数据
    metadata_path = os.path.join(media_library_path, metadata_file)
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    else:
        # 如果没有元数据文件，则创建一个简单的索引
        metadata = index_media_library(media_library_path, metadata_file)
    
    # 搜索匹配的视频
    matched_videos = []
    for keyword in keywords:
        for item in metadata:
            if keyword.lower() in item['tags'] or keyword.lower() in item['description'].lower():
                if item['path'] not in matched_videos:
                    matched_videos.append(item['path'])
    
    # 如果没有找到匹配的视频，返回一些默认视频
    if not matched_videos:
        default_videos = glob.glob(os.path.join(media_library_path, "default", "*.mp4"))
        return default_videos
    
    return matched_videos

def index_media_library(
    media_library_path: str, 
    metadata_file: str = "metadata.json"
) -> List[Dict[str, Any]]:
    """
    索引媒资库中的视频文件并创建元数据
    
    参数：
        media_library_path (str): 媒资库路径
        metadata_file (str): 元数据文件名
        
    返回：
        List[Dict[str, Any]]: 媒资库元数据
    """
    metadata = []
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    
    # 遍历媒资库目录
    for root, _, files in os.walk(media_library_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in video_extensions):
                file_path = os.path.join(root, file)
                # 从文件名和目录结构提取标签和描述
                relative_path = os.path.relpath(root, media_library_path)
                tags = relative_path.split(os.sep) + [os.path.splitext(file)[0]]
                tags = [tag.lower() for tag in tags if tag]
                
                metadata.append({
                    'path': file_path,
                    'tags': tags,
                    'description': ' '.join(tags)
                })
    
    # 保存元数据
    with open(os.path.join(media_library_path, metadata_file), 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    return metadata