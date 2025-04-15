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
            # 获取环境变量，Docker环境中应该使用'db'作为主机名
            db_host = os.getenv('DB_HOST', 'localhost')
            db_name = os.getenv('DB_NAME', 'testiflow_db')
            db_user = os.getenv('DB_USER', 'root')
            db_password = os.getenv('DB_PASSWORD', '147308')
            db_port = int(os.getenv('DB_PORT', 3306))
            
            print(f"尝试连接数据库: {db_host}:{db_port}, 数据库: {db_name}, 用户: {db_user}")
            
            # 添加连接超时和重试设置，解决Docker环境中的网络延迟问题
            self.pool = MySQLConnectionPool(
                pool_name="testiflow_pool",
                pool_size=5,
                host=db_host,
                database=db_name,
                user=db_user,
                password=db_password,
                port=db_port,
                connect_timeout=30,  # 增加连接超时时间
                connection_timeout=30,  # 增加连接超时时间
                use_pure=True,  # 使用纯Python实现，提高兼容性
                auth_plugin='mysql_native_password'  # 指定认证插件
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
            print("数据库连接池未初始化，尝试重新初始化...")
            self._initialize_pool()
            if not self.pool:
                print("数据库连接池初始化失败")
                return None
            
        try:
            conn = self.pool.get_connection()
            print("成功获取数据库连接")
            return conn
        except Error as e:
            print(f"获取数据库连接失败: {e}")
            # 尝试重新初始化连接池
            print("尝试重新初始化数据库连接池...")
            self._initialize_pool()
            try:
                return self.pool.get_connection() if self.pool else None
            except Error as e2:
                print(f"重试获取数据库连接失败: {e2}")
                return None

# 全局数据库配置实例
db_config = DatabaseConfig()