from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `file` (
    `file_id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '文件ID',
    `file_name` VARCHAR(255) NOT NULL COMMENT '原始文件名',
    `source` VARCHAR(500) NOT NULL COMMENT '文件绝对路径',
    `is_delete` BOOL NOT NULL COMMENT '逻辑删除：0-未删除，1-已删除' DEFAULT 0,
    `created_at` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `session_id` BIGINT COMMENT '关联会话（可为空）',
    `user_id` BIGINT NOT NULL COMMENT '上传用户',
    CONSTRAINT `fk_file_session_3157f16b` FOREIGN KEY (`session_id`) REFERENCES `session` (`session_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_file_user_d47b8368` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
    KEY `idx_file_is_dele_1a2899` (`is_delete`),
    KEY `idx_file_session_3283fc` (`session_id`),
    KEY `idx_file_user_id_8217ec` (`user_id`)
) CHARACTER SET utf8mb4 COMMENT='文件表 —— 记录用户上传文件的源路径';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `file`;"""


MODELS_STATE = (
    "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"
    "/fEr/x+vXAbDOugWvbTe5w8BXv4Hzgfiqg=="
)
