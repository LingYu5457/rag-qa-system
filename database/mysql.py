import pymysql
from datetime import datetime
from contextlib import contextmanager
from config.settings import mysql_settings as config
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    """数据库连接管理器"""
    def __init__(self):
        pass

    @contextmanager
    def get_connection(self):
        """获取数据库连接的上下文管理器"""
        connection = pymysql.connect(
            host=config.MYSQL_HOST,
            port=config.MYSQL_PORT,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB_NAME,
            charset=config.MYSQL_DB_CHARSET,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            yield connection
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()

class UserDAO:
    """用户表操作类"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def insert_user(self, user_name: str, user_account: str, user_password: str) -> int:
        """插入新用户，返回用户ID"""
        sql = """
            INSERT INTO user (user_name, user_account, user_password) 
            VALUES (%s, %s, %s)
        """
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (user_name, user_account, user_password))
                return cursor.lastrowid
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """根据用户ID查询用户信息"""
        sql = """
            SELECT user_id, user_name, user_account, is_delete, created_at 
            FROM user 
            WHERE user_id = %s AND is_delete = 0
        """
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (user_id,))
                return cursor.fetchone()
    
    def get_user_by_account(self, user_account: str) -> Optional[Dict]:
        """根据账号查询用户信息（用于登录验证）"""
        sql = """
            SELECT user_id, user_name, user_account, user_password, is_delete 
            FROM user 
            WHERE user_account = %s AND is_delete = 0
        """
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (user_account,))
                return cursor.fetchone()
    
    def update_user(self, user_id: int, **kwargs) -> bool:
        """根据用户ID更新用户信息"""
        allowed_fields = ['user_name', 'user_password', 'user_account']
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not update_fields:
            return False
        
        set_clause = ', '.join([f"{field} = %s" for field in update_fields.keys()])
        sql = f"UPDATE user SET {set_clause} WHERE user_id = %s AND is_delete = 0"
        values = list(update_fields.values()) + [user_id]
        
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                affected_rows = cursor.execute(sql, values)
                return affected_rows > 0
    
    def delete_user(self, user_id: int) -> bool:
        """逻辑删除用户"""
        sql = "UPDATE user SET is_delete = 1 WHERE user_id = %s AND is_delete = 0"
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                affected_rows = cursor.execute(sql, (user_id,))
                return affected_rows > 0


class SessionDAO:
    """会话表操作类"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def insert_session(self, user_id: int, session_title: str = "新对话") -> int:
        """创建新会话，返回会话ID"""
        sql = """
            INSERT INTO session (user_id, session_title) 
            VALUES (%s, %s)
        """
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (user_id, session_title))
                return cursor.lastrowid
    
    def get_session_by_id(self, session_id: int) -> Optional[Dict]:
        """根据会话ID查询会话信息"""
        sql = """
            SELECT session_id, user_id, session_title, is_delete, created_at 
            FROM session 
            WHERE session_id = %s AND is_delete = 0
        """
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (session_id,))
                return cursor.fetchone()
    
    def get_sessions_by_user_id(self, user_id: int) -> List[Dict]:
        """根据用户ID查询该用户的所有会话"""
        sql = """
            SELECT session_id, user_id, session_title, created_at 
            FROM session 
            WHERE user_id = %s AND is_delete = 0 
            ORDER BY created_at DESC
        """
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (user_id,))
                return cursor.fetchall()
    
    def update_session(self, session_id: int, **kwargs) -> bool:
        """根据会话ID更新会话信息（主要是标题）"""
        allowed_fields = ['session_title']
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not update_fields:
            return False
        
        set_clause = ', '.join([f"{field} = %s" for field in update_fields.keys()])
        sql = f"UPDATE session SET {set_clause} WHERE session_id = %s AND is_delete = 0"
        values = list(update_fields.values()) + [session_id]
        
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                affected_rows = cursor.execute(sql, values)
                return affected_rows > 0
    
    def delete_session(self, session_id: int) -> bool:
        """逻辑删除会话"""
        sql = "UPDATE session SET is_delete = 1 WHERE session_id = %s AND is_delete = 0"
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                affected_rows = cursor.execute(sql, (session_id,))
                return affected_rows > 0


class ChatDAO:
    """聊天消息表操作类"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def insert_message(self, session_id: int, role: str, chat_message: str) -> int:
        """插入聊天消息，返回消息ID"""
        sql = """
            INSERT INTO chat (session_id, role, chat_message) 
            VALUES (%s, %s, %s)
        """
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (session_id, role, chat_message))
                return cursor.lastrowid
    
    def get_message_by_id(self, chat_id: int) -> Optional[Dict]:
        """根据消息ID查询消息"""
        sql = """
            SELECT chat_id, session_id, role, chat_message, created_at 
            FROM chat 
            WHERE chat_id = %s AND is_delete = 0
        """
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (chat_id,))
                return cursor.fetchone()
    
    def get_messages_by_session_id(self, session_id: int, limit: int = None) -> List[Dict]:
        """根据会话ID查询该会话的所有消息（按时间排序）"""
        sql = """
            SELECT chat_id, session_id, role, chat_message, created_at 
            FROM chat 
            WHERE session_id = %s AND is_delete = 0 
            ORDER BY created_at ASC
        """
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                if limit:
                    # 【修复点2】使用 %s 占位符处理 LIMIT，比 f-string 安全且规范
                    sql += " LIMIT %s"
                    cursor.execute(sql, (session_id, limit))
                else:
                    cursor.execute(sql, (session_id,))
                return cursor.fetchall()
    
    def update_message(self, chat_id: int, **kwargs) -> bool:
        """根据消息ID更新消息内容"""
        allowed_fields = ['chat_message', 'role']
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not update_fields:
            return False
        
        set_clause = ', '.join([f"{field} = %s" for field in update_fields.keys()])
        sql = f"UPDATE chat SET {set_clause} WHERE chat_id = %s AND is_delete = 0"
        values = list(update_fields.values()) + [chat_id]
        
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                affected_rows = cursor.execute(sql, values)
                return affected_rows > 0
    
    def delete_message(self, chat_id: int) -> bool:
        """逻辑删除消息"""
        sql = "UPDATE chat SET is_delete = 1 WHERE chat_id = %s AND is_delete = 0"
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                affected_rows = cursor.execute(sql, (chat_id,))
                return affected_rows > 0
    
    def delete_messages_by_session(self, session_id: int) -> bool:
        """逻辑删除某个会话下的所有消息"""
        sql = "UPDATE chat SET is_delete = 1 WHERE session_id = %s AND is_delete = 0"
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                affected_rows = cursor.execute(sql, (session_id,))
                return affected_rows > 0
    
    def get_recent_messages(self, session_id: int, limit: int = 10) -> List[Dict]:
        """获取会话的最近N条消息（用于LangChain上下文窗口）"""
        sql = """
            SELECT role, chat_message 
            FROM (
                SELECT role, chat_message, created_at 
                FROM chat 
                WHERE session_id = %s AND is_delete = 0 
                ORDER BY created_at DESC 
                LIMIT %s
            ) AS recent 
            ORDER BY created_at ASC
        """
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (session_id, limit))
                return cursor.fetchall()