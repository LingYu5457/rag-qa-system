from tortoise import fields
from tortoise.models import Model


class User(Model):
    """用户表"""
    user_id = fields.BigIntField(pk=True, description='用户ID')
    user_name = fields.CharField(max_length=50, description='用户名')
    user_account = fields.CharField(
        max_length=50, 
        unique=True,  # 创建唯一索引 uk_user_account
        description='登录账号'
    )
    user_password = fields.CharField(max_length=255, description='密码(加密存储)')
    is_delete = fields.BooleanField(
        default=False, 
        index=True,  # 创建普通索引 idx_is_delete
        description='逻辑删除：0-未删除，1-已删除'
    )
    created_at = fields.DatetimeField(auto_now_add=True, description='创建时间')
    
    sessions: fields.ReverseRelation["Session"]
    files: fields.ReverseRelation["File"]
    
    class Meta:
        table = "user"
        ordering = ["-created_at"]


class Session(Model):
    """会话表"""
    session_id = fields.BigIntField(pk=True, description='会话ID')
    user = fields.ForeignKeyField(
        'models.User', 
        related_name='sessions',
        index=True,  # 外键会自动创建索引 idx_user_id
        description='关联用户'
    )
    session_title = fields.CharField(
        max_length=100, 
        default='新对话', 
        description='会话标题'
    )
    is_delete = fields.BooleanField(
        default=False, 
        index=True,  # 创建普通索引 idx_is_delete
        description='逻辑删除：0-未删除，1-已删除'
    )
    created_at = fields.DatetimeField(auto_now_add=True, description='创建时间')
    
    chats: fields.ReverseRelation["Chat"]
    files: fields.ReverseRelation["File"]

    class Meta:
        table = "session"
        ordering = ["-created_at"]


class Chat(Model):
    """聊天消息表"""
    files: fields.ReverseRelation["File"]
    chat_id = fields.BigIntField(pk=True, description='消息ID')
    session = fields.ForeignKeyField(
        'models.Session',
        related_name='chats',
        index=True,  # 外键会自动创建索引 idx_session_id
        description='关联会话'
    )
    role = fields.CharField(max_length=20, description='角色：system/ai/human')
    chat_message = fields.TextField(description='消息内容')
    is_delete = fields.BooleanField(
        default=False, 
        index=True,  # 创建普通索引 idx_is_delete
        description='逻辑删除：0-未删除，1-已删除'
    )
    created_at = fields.DatetimeField(auto_now_add=True, description='创建时间')
    
    class Meta:
        table = "chat"
        ordering = ["created_at"]  # 消息按时间正序

class File(Model):
    """文件表 —— 记录用户上传文件的源路径"""
    file_id = fields.BigIntField(pk=True, description='文件ID')
    user = fields.ForeignKeyField(
        'models.User',
        related_name='files',
        index=True,
        description='上传用户'
    )
    session = fields.ForeignKeyField(
        'models.Session',
        related_name='files',
        null=True,
        index=True,
        description='关联会话（可为空）'
    )
    chat = fields.ForeignKeyField(
        'models.Chat',
        related_name='files',
        null=True,
        index=True,
        description='关联聊天消息（记录在chat里的位置）'
    )
    file_name = fields.CharField(max_length=255, description='原始文件名')
    is_rag = fields.BooleanField(
        default=False,
        description='是否为RAG文件'
    )
    source = fields.CharField(max_length=500, description='文件绝对路径')
    is_delete = fields.BooleanField(
        default=False,
        index=True,
        description='逻辑删除：0-未删除，1-已删除'
    )
    created_at = fields.DatetimeField(auto_now_add=True, description='创建时间')

    class Meta:
        table = "file"
        ordering = ["-created_at"]