import os
from typing import Optional
import mysql.connector
from mysql.connector import Error
from mysql.connector.pooling import MySQLConnectionPool

class DatabaseConfig:
    """
    数据库配置类，用于管理MySQL数据库连接
    """
    
    def __init__(self):
        self.pool = None
        self._initialize_pool()
    
    def _initialize_pool(self):
        """初始化数据库连接池"""
        try:
            self.pool = MySQLConnectionPool(
                pool_name="testiflow_pool",
                pool_size=5,
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'testiflow_db'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', '147308'),
                port=os.getenv('DB_PORT', 3306)
            )
            
            # 初始化数据库表结构
            conn = self.pool.get_connection()
            cursor = conn.cursor()
            
            # 创建outlines表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS outlines (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    created_at DATETIME NOT NULL,
                    updated_at DATETIME NOT NULL
                )""")
            
            # 创建outline_sections表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS outline_sections (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    outline_id INT NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    content TEXT,
                    FOREIGN KEY (outline_id) REFERENCES outlines(id) ON DELETE CASCADE
                )""")
            
            # 创建scripts表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scripts (
                    id VARCHAR(36) PRIMARY KEY,
                    outline_id INT NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME NOT NULL,
                    FOREIGN KEY (outline_id) REFERENCES outlines(id) ON DELETE CASCADE
                )""")
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print("数据库连接池初始化成功")
        except Error as e:
            print(f"数据库连接池初始化失败: {e}")
    
    def get_connection(self) -> Optional[mysql.connector.MySQLConnection]:
        """从连接池获取数据库连接"""
        if not self.pool:
            self._initialize_pool()
            
        try:
            return self.pool.get_connection()
        except Error as e:
            print(f"获取数据库连接失败: {e}")
            return None

# 全局数据库配置实例
db_config = DatabaseConfig()