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
    def get_outline_by_id(outline_id: str) -> Optional[Outline]:
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
                
    @staticmethod
    def get_outline_list(page: int, size: int) -> dict:
        """
        获取提纲列表(分页)
        :param page: 页码
        :param size: 每页数量
        :return: 包含数据和总数的字典
        """
        conn = None
        try:
            conn = db_config.get_connection()
            if not conn:
                return {'data': [], 'total': 0}
                
            cursor = conn.cursor(dictionary=True)
            
            # 计算偏移量
            offset = (page - 1) * size
            
            # 查询总数
            cursor.execute("SELECT COUNT(*) AS total FROM outlines")
            total = cursor.fetchone()['total']
            
            # 查询分页数据
            cursor.execute(
                """
                SELECT id, title, created_at, updated_at FROM outlines
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
                """,
                (size, offset)
            )
            
            data = cursor.fetchall()
            
            # 转换ID为字符串
            for item in data:
                item['id'] = str(item['id'])
            
            return {
                'data': data,
                'total': total
            }
            
        except Error as e:
            print(f"获取提纲列表失败: {e}")
            return {'data': [], 'total': 0}
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
                
    @staticmethod
    def get_script_list(page: int, size: int) -> dict:
        """
        获取脚本列表(分页)
        :param page: 页码
        :param size: 每页数量
        :return: 包含数据和总数的字典
        """
        conn = None
        try:
            conn = db_config.get_connection()
            if not conn:
                return {'data': [], 'total': 0}
                
            cursor = conn.cursor(dictionary=True)
            
            # 计算偏移量
            offset = (page - 1) * size
            
            # 查询总数
            cursor.execute("SELECT COUNT(*) AS total FROM scripts")
            total = cursor.fetchone()['total']
            
            # 查询分页数据
            cursor.execute(
                """
                SELECT s.id, s.outline_id, s.created_at, o.title as outline_title 
                FROM scripts s
                LEFT JOIN outlines o ON s.outline_id = o.id
                ORDER BY s.created_at DESC
                LIMIT %s OFFSET %s
                """,
                (size, offset)
            )
            
            data = cursor.fetchall()
            
            # 转换ID为字符串
            for item in data:
                item['id'] = str(item['id'])
                item['outline_id'] = str(item['outline_id'])
            
            return {
                'data': data,
                'total': total
            }
            
        except Error as e:
            print(f"获取脚本列表失败: {e}")
            return {'data': [], 'total': 0}
        finally:
            if conn:
                conn.close()