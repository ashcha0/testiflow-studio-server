from datetime import datetime
from typing import List, Optional
import mysql.connector
from mysql.connector import Error
from .config import db_config
from .models import Outline, OutlineSection, Script

class OutlineOperations:
    """
    提纲数据库操作类
    """
    
    @staticmethod
    def create_outline(outline: Outline) -> Optional[str]:
        """
        创建新提纲
        :param outline: 提纲对象
        :return: 提纲ID
        """
        conn = None
        try:
            conn = db_config.get_connection()
            if not conn:
                return None
                
            cursor = conn.cursor(dictionary=True)
            
            # 插入提纲主表
            cursor.execute(
                """
                INSERT INTO outlines (title, created_at, updated_at)
                VALUES (%s, %s, %s)
                """,
                (outline.title, outline.created_at, outline.updated_at)
            )
            outline_id = cursor.lastrowid
            
            # 插入提纲章节
            for section in outline.sections:
                cursor.execute(
                    """
                    INSERT INTO outline_sections 
                    (outline_id, title, content)
                    VALUES (%s, %s, %s)
                    """,
                    (outline_id, section.title, section.content)
                )
            
            conn.commit()
            return str(outline_id)
            
        except Error as e:
            print(f"创建提纲失败: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def get_outline(outline_id: str) -> Optional[Outline]:
        """
        获取提纲详情
        :param outline_id: 提纲ID
        :return: 提纲对象
        """
        conn = None
        try:
            conn = db_config.get_connection()
            if not conn:
                return None
                
            cursor = conn.cursor(dictionary=True)
            
            # 查询提纲主表
            cursor.execute(
                """
                SELECT * FROM outlines 
                WHERE id = %s
                """,
                (outline_id,)
            )
            outline_data = cursor.fetchone()
            
            if not outline_data:
                return None
            
            # 查询提纲章节
            cursor.execute(
                """
                SELECT * FROM outline_sections
                WHERE outline_id = %s
                ORDER BY id
                """,
                (outline_id,)
            )
            sections_data = cursor.fetchall()
            
            # 构建提纲对象
            outline = Outline(
                outline_id=str(outline_data['id']),
                title=outline_data['title'],
                created_at=outline_data['created_at'],
                updated_at=outline_data['updated_at']
            )
            
            # 构建章节列表
            for section_data in sections_data:
                outline.sections.append(
                    OutlineSection(
                        section_id=section_data['id'],
                        title=section_data['title'],
                        content=section_data['content']
                    )
                )
            
            return outline
            
        except Error as e:
            print(f"获取提纲失败: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def update_outline(outline: Outline) -> bool:
        """
        更新提纲
        :param outline: 提纲对象
        :return: 是否成功
        """
        conn = None
        try:
            conn = db_config.get_connection()
            if not conn:
                return False
                
            cursor = conn.cursor(dictionary=True)
            
            # 更新提纲主表
            cursor.execute(
                """
                UPDATE outlines 
                SET title = %s, updated_at = %s
                WHERE id = %s
                """,
                (outline.title, datetime.now(), outline.outline_id)
            )
            
            # 删除原有章节
            cursor.execute(
                """
                DELETE FROM outline_sections
                WHERE outline_id = %s
                """,
                (outline.outline_id,)
            )
            
            # 插入新章节
            for section in outline.sections:
                cursor.execute(
                    """
                    INSERT INTO outline_sections 
                    (outline_id, title, content)
                    VALUES (%s, %s, %s)
                    """,
                    (outline.outline_id, section.title, section.content)
                )
            
            conn.commit()
            return True
            
        except Error as e:
            print(f"更新提纲失败: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()

class ScriptOperations:
    """
    脚本数据库操作类
    """
    
    @staticmethod
    def create_script(script: Script) -> bool:
        """
        创建脚本
        :param script: 脚本对象
        :return: 是否成功
        """
        conn = None
        try:
            conn = db_config.get_connection()
            if not conn:
                return False
                
            cursor = conn.cursor()
            
            cursor.execute(
                """
                INSERT INTO scripts 
                (id, outline_id, content, created_at)
                VALUES (%s, %s, %s, %s)
                """,
                (script.script_id, script.outline_id, script.content, script.created_at)
            )
            
            conn.commit()
            return True
            
        except Error as e:
            print(f"创建脚本失败: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def get_script(script_id: str) -> Optional[Script]:
        """
        获取脚本
        :param script_id: 脚本ID
        :return: 脚本对象
        """
        conn = None
        try:
            conn = db_config.get_connection()
            if not conn:
                return None
                
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                """
                SELECT * FROM scripts 
                WHERE id = %s
                """,
                (script_id,)
            )
            
            script_data = cursor.fetchone()
            if not script_data:
                return None
            
            return Script(
                script_id=script_data['id'],
                outline_id=script_data['outline_id'],
                content=script_data['content'],
                created_at=script_data['created_at']
            )
            
        except Error as e:
            print(f"获取脚本失败: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def get_script_by_outline(outline_id: str) -> Optional[Script]:
        """
        根据提纲ID获取脚本
        :param outline_id: 提纲ID
        :return: 脚本对象
        """
        conn = None
        try:
            conn = db_config.get_connection()
            if not conn:
                return None
                
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                """
                SELECT * FROM scripts 
                WHERE outline_id = %s
                """,
                (outline_id,)
            )
            
            script_data = cursor.fetchone()
            if not script_data:
                return None
            
            return Script(
                script_id=script_data['id'],
                outline_id=script_data['outline_id'],
                content=script_data['content'],
                created_at=script_data['created_at']
            )
            
        except Error as e:
            print(f"获取脚本失败: {e}")
            return None
        finally:
            if conn:
                conn.close()