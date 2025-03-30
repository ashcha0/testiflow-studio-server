from datetime import datetime
from typing import List, Optional

class OutlineSection:
    """
    提纲章节模型
    """
    def __init__(self, 
                 title: str, 
                 content: Optional[str] = None,
                 section_id: Optional[int] = None):
        self.section_id = section_id
        self.title = title
        self.content = content

class Outline:
    """
    视频提纲模型
    """
    def __init__(self, 
                 title: str, 
                 outline_id: Optional[str] = None,
                 sections: Optional[List[OutlineSection]] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        self.outline_id = outline_id
        self.title = title
        self.sections = sections or []
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

class Script:
    """
    视频脚本模型
    """
    def __init__(self, 
                 script_id: str, 
                 outline_id: str,
                 content: str,
                 created_at: Optional[datetime] = None):
        self.script_id = script_id
        self.outline_id = outline_id
        self.content = content
        self.created_at = created_at or datetime.now()